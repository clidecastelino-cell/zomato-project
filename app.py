# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
from datasets import load_dataset
import json
import os
from dotenv import load_dotenv
from groq import Groq, APIStatusError

load_dotenv()

def categorize_cost(cost):
    if pd.isna(cost):
        return 'Medium'
    elif cost < 500:
        return 'Low'
    elif cost < 1500:
        return 'Medium'
    else:
        return 'High'

@st.cache_data
def load_data():
    try:
        # 1. Fetch data from Hugging Face
        dataset = load_dataset('ManikaSaini/zomato-restaurant-recommendation', split='train')
        
        # Drop heavy unused columns before converting to pandas to save memory
        cols_to_keep = ['name', 'location', 'cuisines', 'rate', 'approx_cost(for two people)']
        cols_to_remove = [col for col in dataset.column_names if col not in cols_to_keep]
        dataset = dataset.remove_columns(cols_to_remove)
        
        df = dataset.to_pandas() # type: ignore
        
        # 2. Data Cleaning
        # Lowercase columns for consistency
        df = df.rename(columns=lambda x: str(x).lower().strip())
        
        # Drop rows missing crucial information
        required_cols = ['name', 'location', 'cuisines']
        existing_required = [col for col in required_cols if col in df.columns]
        if existing_required:
            df = df.dropna(subset=existing_required)
        
        # Remove duplicate restaurants (same name + location)
        df = df.drop_duplicates(subset=['name', 'location'], keep='first')
        
        # Parse cuisines into lists (assuming it's a comma-separated string)
        if 'cuisines' in df.columns:
            df['cuisines'] = df['cuisines'].apply(lambda x: [c.strip() for c in str(x).split(',')] if pd.notna(x) else [])
            
        # Categorize numeric costs into "low", "medium", "high" buckets
        cost_col = None
        for col in df.columns:
            if 'cost' in col:
                cost_col = col
                break
                
        if cost_col:
            # Clean cost strings (e.g., "1,200" -> 1200)
            df[cost_col] = df[cost_col].astype(str).str.replace(',', '', regex=False)
            df[cost_col] = pd.to_numeric(df[cost_col], errors='coerce')
            
            # Fill missing costs with median
            median_cost = df[cost_col].median()
            df[cost_col] = df[cost_col].fillna(median_cost)
            
            # Categorize
            df['cost_category'] = df[cost_col].apply(categorize_cost)
            
        # Standardize rating if it exists
        rating_col = None
        for col in df.columns:
            if 'rating' in col or 'rate' in col:
                rating_col = col
                break
                
        if rating_col and pd.api.types.is_string_dtype(df[rating_col]):
            # Often ratings are in format "4.1/5" or "NEW"
            df[rating_col] = df[rating_col].astype(str).str.split('/').str[0]
            df[rating_col] = pd.to_numeric(df[rating_col], errors='coerce')
            df[rating_col] = df[rating_col].fillna(0)
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍽️", layout="wide")
    st.title("🍽️ AI-Powered Restaurant Recommender")
    st.markdown("Welcome to the Zomato Restaurant Recommendation System.")
    
    with st.spinner("Loading and preprocessing restaurant data..."):
        df = load_data()
        
    if df.empty:
        st.warning("No data available.")
        return
        
    # Dataset Preview
    with st.expander("Dataset Preview"):
        st.dataframe(df.head())
        
    # Load API key from environment
    api_key = os.environ.get("GROQ_API_KEY", "")
    
    # Phase 3: UI Skeleton
    # Sidebar for Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        st.write("Data powered by Zomato & HuggingFace")

    # Main area for User Preferences
    st.header("🎯 Your Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Location (Dropdown dynamically populated)
        locations = sorted(df['location'].dropna().unique().tolist())
        selected_location = st.selectbox("Location", options=["Any"] + locations)
        
        # Budget (Select Box)
        # Categorized as Low, Medium, High in Phase 2
        selected_budget = st.selectbox("Budget", options=["Any", "Low", "Medium", "High"])
        
    with col2:
        # Minimum Rating (Slider)
        rating_col = None
        for col in df.columns:
            if 'rating' in col or 'rate' in col:
                rating_col = col
                break
        
        max_rating = 5.0
        if rating_col:
            numeric_ratings = pd.to_numeric(df[rating_col], errors='coerce')
            max_val = numeric_ratings.max()
            if not pd.isna(max_val) and max_val > 0:
                max_rating = float(max_val)
                
        selected_rating = st.slider("Minimum Rating", min_value=0.0, max_value=max_rating, value=3.5, step=0.1)
        
        # Cuisine (Multiselect)
        # Extract unique cuisines
        all_cuisines = set()
        if 'cuisines' in df.columns:
            for cuisine_list in df['cuisines']:
                all_cuisines.update(cuisine_list)
        all_cuisines = sorted(list(all_cuisines))
        
        selected_cuisines = st.multiselect("Preferred Cuisines", options=all_cuisines)
        
    # Additional Preferences
    additional_prefs = st.text_area("Additional Preferences (Optional)", 
                                    placeholder="e.g., family-friendly, romantic ambiance, rooftop seating, vegan options...")
    
    # Recommendation Button
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Filtering restaurants..."):
            filtered_df = df.copy()
            
            # 1. Location Filter
            if selected_location != "Any":
                # Ensure we use 'location' column for filtering as specified
                filtered_df = filtered_df[filtered_df['location'] == selected_location]
                
            # 2. Budget Filter
            if selected_budget != "Any":
                filtered_df = filtered_df[filtered_df['cost_category'] == selected_budget]
                
            # 3. Rating Filter
            if rating_col:
                filtered_df[rating_col] = pd.to_numeric(filtered_df[rating_col], errors='coerce')
                filtered_df = filtered_df[filtered_df[rating_col] >= selected_rating]
                
            # 4. Cuisine Filter
            if selected_cuisines:
                filtered_df = filtered_df[filtered_df['cuisines'].apply(lambda c_list: any(c in c_list for c in selected_cuisines))]
                
            if filtered_df.empty:
                st.warning("No restaurants match your exact preferences. Try relaxing your filters!")
                return
                
            # Sort by rating and get top N
            if rating_col:
                filtered_df = filtered_df.sort_values(by=rating_col, ascending=False)
                
            top_candidates = filtered_df.head(5)
            
            st.success(f"Found {len(filtered_df)} matches! Analyzing the top {len(top_candidates)} options...")
            
            with st.expander("Top Candidates (Pre-AI Filter)", expanded=True):
                # Format cuisines list to string for display
                display_df = top_candidates.copy()
                display_df['cuisines'] = display_df['cuisines'].apply(lambda x: ", ".join(x))
                cols_to_show = ['name', 'location', 'cuisines', 'cost_category']
                if rating_col:
                    cols_to_show.append(rating_col)
                st.dataframe(display_df[cols_to_show], use_container_width=True)
                
            # Phase 5: AI Recommendation Engine (LLM Layer)
            if not api_key:
                st.error("GROQ_API_KEY not found. Please set it in your .env file.")
            else:
                try:
                    client = Groq(api_key=api_key)
                    
                    # Prepare lean context (only relevant columns to stay within token limits)
                    cols_for_ai = ['name', 'location', 'cuisines', 'cost_category']
                    if rating_col:
                        cols_for_ai.append(rating_col)
                    ai_df = top_candidates[cols_for_ai].copy()
                    ai_df['cuisines'] = ai_df['cuisines'].apply(lambda x: ", ".join(x))
                    candidates_json = ai_df.to_dict(orient="records")
                    
                    system_prompt = """You are an expert food concierge. Your task is to recommend the best 3-5 restaurants from the provided list based on the user's preferences.
You must return your response in valid JSON format with a single key 'recommendations'. Its value must be an array of objects.
Each object should have: 'name', 'rating', 'cost', 'cuisines', and 'explanation' (a personalized explanation of why it's a good fit based on the user's preferences)."""
                    
                    user_prefs = additional_prefs if additional_prefs else "Best overall options from the list"
                    user_prompt = f"User Preferences: {user_prefs}\n\nCandidate Restaurants: {json.dumps(candidates_json)}"
                    
                    with st.spinner("AI is analyzing the top choices for you..."):
                        response = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            response_format={"type": "json_object"},
                            temperature=0.7,
                            max_tokens=1024
                        )
                        
                        result_str = response.choices[0].message.content
                        if result_str:
                            try:
                                result_json = json.loads(result_str)
                            except json.JSONDecodeError:
                                st.error("AI returned an invalid response format. Please try again.")
                                return
                            
                            recommendations = result_json.get('recommendations', [])
                            if not recommendations:
                                st.warning("AI did not return any recommendations. Try adjusting your preferences.")
                                return
                            
                            st.subheader("🌟 AI Recommendations")
                            for rec in recommendations:
                                with st.container():
                                    st.markdown(f"### {rec.get('name', 'Unknown')}")
                                    st.write(f"**Rating:** {rec.get('rating', 'N/A')} | **Cost:** {rec.get('cost', 'N/A')} | **Cuisines:** {rec.get('cuisines', 'N/A')}")
                                    st.info(rec.get('explanation', 'No explanation provided.'))
                                    st.markdown("---")
                        else:
                            st.error("No response from Groq API.")
                            
                except APIStatusError as e:
                    if e.status_code == 413:
                        st.error("Request too large for the model's token limit. Try narrowing your filters.")
                    elif e.status_code == 401:
                        st.error("🔑 Invalid API key. Please check your GROQ_API_KEY in the .env file.")
                    elif e.status_code == 404:
                        st.error("The AI model is currently unavailable. Please try again later.")
                    elif e.status_code == 429:
                        st.error("⏳ Rate limit exceeded. Please wait a moment and try again.")
                    else:
                        st.error(f"API error ({e.status_code}): {e.message}")
                except Exception as e:
                    st.error(f"Unexpected error during AI recommendation: {e}")

if __name__ == "__main__":
    main()
