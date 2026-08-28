"""
Recommendation engine.

Handles two responsibilities:
1. Filtering the dataset based on user preferences (location, budget, rating, cuisines)
2. Calling the Groq LLM to generate personalized AI recommendations from the filtered candidates
"""

import json
import os
import logging

import pandas as pd
from groq import Groq, APIStatusError

from app.data_loader import get_rating_column
from app.models import RecommendationItem

logger = logging.getLogger(__name__)

# System prompt for the Groq LLM
SYSTEM_PROMPT = """You are an expert food concierge. Your task is to recommend the best 3-5 restaurants from the provided list based on the user's preferences.
You must return your response in valid JSON format with a single key 'recommendations'. Its value must be an array of objects.
Each object should have: 'name', 'rating', 'cost', 'cuisines', and 'explanation' (a personalized explanation of why it's a good fit based on the user's preferences)."""


def filter_restaurants(
    df: pd.DataFrame,
    location: str = "Any",
    budget: str = "Any",
    min_rating: float = 0.0,
    cuisines: list[str] | None = None,
) -> pd.DataFrame:
    """
    Apply hard filters to the dataset based on user preferences.

    Returns a filtered DataFrame sorted by rating (descending).
    """
    filtered = df.copy()

    # 1. Location filter
    if location != "Any":
        filtered = filtered[filtered["location"] == location]

    # 2. Budget filter
    if budget != "Any" and "cost_category" in filtered.columns:
        filtered = filtered[filtered["cost_category"] == budget]

    # 3. Rating filter
    rating_col = get_rating_column(filtered)
    if rating_col:
        filtered[rating_col] = pd.to_numeric(filtered[rating_col], errors="coerce")
        filtered = filtered[filtered[rating_col] >= min_rating]

    # 4. Cuisine filter
    if cuisines:
        filtered = filtered[
            filtered["cuisines"].apply(
                lambda c_list: any(c in c_list for c in cuisines)
                if isinstance(c_list, list)
                else False
            )
        ]

    # Sort by rating descending
    if rating_col:
        filtered = filtered.sort_values(by=rating_col, ascending=False)

    return filtered


def get_ai_recommendations(
    candidates_df: pd.DataFrame,
    additional_preferences: str = "",
) -> list[RecommendationItem]:
    """
    Send the top candidate restaurants to Groq LLM for personalized ranking.

    Returns a list of RecommendationItem objects.
    Raises ValueError if the API key is missing.
    Raises RuntimeError for API or parsing errors.
    """
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # Prepare lean context for the LLM (only relevant columns)
    rating_col = get_rating_column(candidates_df)
    cols_for_ai = ["name", "location", "cuisines", "cost_category"]
    if rating_col:
        cols_for_ai.append(rating_col)

    ai_df = candidates_df[cols_for_ai].copy()
    ai_df["cuisines"] = ai_df["cuisines"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else str(x)
    )
    candidates_json = ai_df.to_dict(orient="records")

    # Build user prompt
    user_prefs = additional_preferences if additional_preferences else "Best overall options from the list"
    user_prompt = f"User Preferences: {user_prefs}\n\nCandidate Restaurants: {json.dumps(candidates_json)}"

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1024,
        )

        result_str = response.choices[0].message.content
        if not result_str:
            raise RuntimeError("No response content from Groq API.")

        result_json = json.loads(result_str)
        raw_recommendations = result_json.get("recommendations", [])

        if not raw_recommendations:
            raise RuntimeError("AI did not return any recommendations.")

        # Parse into Pydantic models
        recommendations = [
            RecommendationItem(
                name=rec.get("name", "Unknown"),
                rating=rec.get("rating"),
                cost=rec.get("cost"),
                cuisines=rec.get("cuisines"),
                explanation=rec.get("explanation", "No explanation provided."),
            )
            for rec in raw_recommendations
        ]

        return recommendations

    except APIStatusError as e:
        error_messages = {
            413: "Request too large for the model's token limit. Try narrowing your filters.",
            401: "Invalid API key. Please check your GROQ_API_KEY.",
            404: "The AI model is currently unavailable. Please try again later.",
            429: "Rate limit exceeded. Please wait a moment and try again.",
        }
        message = error_messages.get(
            e.status_code, f"API error ({e.status_code}): {e.message}"
        )
        raise RuntimeError(message) from e

    except json.JSONDecodeError as e:
        raise RuntimeError("AI returned an invalid response format.") from e
