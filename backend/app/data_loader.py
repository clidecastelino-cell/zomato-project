"""
Data ingestion and caching layer.

Loads the Zomato restaurant dataset from HuggingFace, cleans it,
and caches the result in memory so subsequent requests are instant.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Module-level cache — loaded once when the first request hits
_cached_df: pd.DataFrame | None = None


def categorize_cost(cost) -> str:
    """Bucket a numeric cost value into Low / Medium / High."""
    if pd.isna(cost):
        return "Medium"
    elif cost < 500:
        return "Low"
    elif cost < 1500:
        return "Medium"
    else:
        return "High"


def _find_column(df: pd.DataFrame, keyword: str) -> str | None:
    """Find the first column whose name contains the given keyword."""
    for col in df.columns:
        if keyword in col:
            return col
    return None


def load_data() -> pd.DataFrame:
    """
    Fetch, clean, and cache the Zomato dataset from HuggingFace.

    Returns a cleaned pandas DataFrame. Uses module-level caching so the
    dataset is only downloaded and processed once per server lifetime.
    """
    global _cached_df

    if _cached_df is not None:
        return _cached_df

    logger.info("Loading dataset from HuggingFace (first request)...")

    try:
        import os
        # 1. Load pre-downloaded dataset from local CSV file to save memory
        file_path = os.path.join(os.path.dirname(__file__), 'zomato_cleaned.csv')
        df = pd.read_csv(file_path)

        # 2. Data Cleaning
        # Lowercase columns for consistency
        df = df.rename(columns=lambda x: str(x).lower().strip())

        # Drop rows missing crucial information
        required_cols = ["name", "location", "cuisines"]
        existing_required = [col for col in required_cols if col in df.columns]
        if existing_required:
            df = df.dropna(subset=existing_required)

        # Remove duplicate restaurants (same name + location)
        df = df.drop_duplicates(subset=["name", "location"], keep="first")

        # Parse cuisines into lists (comma-separated string → list)
        if "cuisines" in df.columns:
            df["cuisines"] = df["cuisines"].apply(
                lambda x: [c.strip() for c in str(x).split(",")]
                if pd.notna(x)
                else []
            )

        # Categorize numeric costs into "Low", "Medium", "High" buckets
        cost_col = _find_column(df, "cost")
        if cost_col:
            # Clean cost strings (e.g., "1,200" -> 1200)
            df[cost_col] = (
                df[cost_col].astype(str).str.replace(",", "", regex=False)
            )
            df[cost_col] = pd.to_numeric(df[cost_col], errors="coerce")

            # Fill missing costs with median
            median_cost = df[cost_col].median()
            df[cost_col] = df[cost_col].fillna(median_cost)

            # Categorize
            df["cost_category"] = df[cost_col].apply(categorize_cost)

        # Standardize rating if it exists
        rating_col = _find_column(df, "rating") or _find_column(df, "rate")
        if rating_col and pd.api.types.is_string_dtype(df[rating_col]):
            # Ratings often in format "4.1/5" or "NEW"
            df[rating_col] = df[rating_col].astype(str).str.split("/").str[0]
            df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
            df[rating_col] = df[rating_col].fillna(0)

        _cached_df = df
        logger.info(f"Dataset loaded successfully: {len(df)} restaurants")
        return df

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame()


def get_rating_column(df: pd.DataFrame) -> str | None:
    """Return the name of the rating column, or None if not found."""
    return _find_column(df, "rating") or _find_column(df, "rate")


def get_available_filters(df: pd.DataFrame) -> dict:
    """
    Extract the available filter options from the loaded dataset.

    Returns a dict with locations, cuisines, and max_rating —
    used to populate the frontend dropdowns.
    """
    # Locations
    locations = sorted(df["location"].dropna().unique().tolist())

    # Unique cuisines (flattened from lists)
    all_cuisines: set[str] = set()
    if "cuisines" in df.columns:
        for cuisine_list in df["cuisines"]:
            if isinstance(cuisine_list, list):
                all_cuisines.update(cuisine_list)
    cuisines = sorted(list(all_cuisines))

    # Max rating
    rating_col = get_rating_column(df)
    max_rating = 5.0
    if rating_col:
        numeric_ratings = pd.to_numeric(df[rating_col], errors="coerce")
        max_val = numeric_ratings.max()
        if not pd.isna(max_val) and max_val > 0:
            max_rating = float(max_val)

    return {
        "locations": locations,
        "cuisines": cuisines,
        "max_rating": max_rating,
    }
