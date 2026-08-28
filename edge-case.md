# Edge Cases & Mitigation Strategies

This document maps potential edge cases and their mitigation strategies to the specific phases outlined in our `implementation-plan.md` and the components in `architecture.md`.

## Phase 1 & 2: Data Ingestion & Preprocessing

### 1. Dataset API Unavailability or Rate Limiting
- **Context:** Fetching `ManikaSaini/zomato-restaurant-recommendation` via Hugging Face `datasets`.
- **Edge Case:** The Hugging Face API is down, times out, or the user hits a rate limit.
- **Mitigation:** Wrap the data loading logic in a `try...except` block. Use Streamlit's `@st.cache_data` to ensure successful loads are cached across sessions. Display a friendly `st.error()` explaining the issue to the user instead of letting the app crash.

### 2. Missing, Corrupted, or Unexpected Data Formats
- **Context:** Converting the raw dataset to a Pandas DataFrame.
- **Edge Case:** Critical fields (Cost, Rating, Cuisines, Location) contain `NaN`, empty strings, or mismatched types.
- **Mitigation:** Implement strict data cleaning during Phase 2:
  - Drop rows where `Restaurant Name` or `Location` is missing.
  - Impute numeric fields (e.g., Cost, Rating) with the column median.
  - Fill missing text fields (e.g., Cuisine) with a placeholder like "Not Specified".

## Phase 3 & 4: UI & Integration Layer (Filtering)

### 3. Overly Restrictive Constraints (Zero Results)
- **Context:** The Pandas boolean filtering logic.
- **Edge Case:** The user inputs a combination of filters (e.g., Minimum Rating = 4.9, Budget = Low, Cuisine = French) that yields an empty DataFrame.
- **Mitigation:** Check `len(filtered_df) == 0`. If true, halt the pipeline before calling the LLM and display a warning via `st.warning()` suggesting the user relax their criteria (e.g., lower the rating or change the budget).

### 4. Overly Broad Constraints (Context Window Overflow)
- **Context:** Formatting candidates for the LLM.
- **Edge Case:** Filtering returns hundreds or thousands of restaurants. Sending all of them to the Gemini LLM will exceed token limits and increase latency/costs.
- **Mitigation:** Enforce a strict limit. Sort the filtered DataFrame by Rating (descending) or Popularity, and extract only the **Top N** (e.g., 10 or 15) candidate restaurants to send in the prompt.

## Phase 5: AI Recommendation Engine (LLM Layer)

### 5. Invalid, Missing, or Exhausted API Credentials
- **Context:** Initializing the `google-genai` client.
- **Edge Case:** The API key provided in the sidebar is blank, invalid, or has exhausted its quota.
- **Mitigation:** Catch authentication exceptions. Do not render a raw traceback. Instead, use `st.error()` to prompt the user to check their API key in the sidebar.

### 6. LLM Hallucinations (Out-of-Dataset Recommendations)
- **Context:** The LLM generating recommendations based on the Top N candidates.
- **Edge Case:** The LLM recommends a famous restaurant it knows from its training data, but which is *not* in the provided candidate list.
- **Mitigation:** Implement strict Prompt Engineering: *"You MUST ONLY recommend restaurants from the provided JSON list. Do not invent or include any external restaurants."*

### 7. Malformed LLM Output / Parsing Failure
- **Context:** Extracting structured data from the LLM's response for the UI.
- **Edge Case:** The LLM outputs conversational text instead of the requested JSON schema, causing the UI rendering logic to throw a `KeyError` or JSON decode error.
- **Mitigation:** 
  - Utilize Gemini's native structured output capabilities (e.g., passing a Pydantic schema) if supported by the SDK version.
  - Implement regex fallback to extract JSON blocks from Markdown.
  - If parsing fails entirely, gracefully fall back to displaying the LLM's raw markdown response in a generic Streamlit text container.

## Phase 6: Output Display & Edge Interactions

### 8. Nonsensical "Additional Preferences"
- **Context:** The free-text input area in the UI.
- **Edge Case:** The user types irrelevant queries (e.g., "Write me a poem", "Where can I buy shoes?").
- **Mitigation:** Include instructions in the System Prompt to ignore off-topic requests, remind the user of the app's purpose, and simply provide the best general restaurant recommendations based on the structured filters.
