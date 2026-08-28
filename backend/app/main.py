"""
FastAPI entry point for the Zomato AI Restaurant Recommender API.

Serves three endpoints:
  GET  /api/health    — Health check for Railway
  GET  /api/filters   — Available filter options (locations, cuisines, max rating)
  POST /api/recommend — AI-powered restaurant recommendations
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.data_loader import load_data, get_available_filters
from app.recommender import filter_restaurants, get_ai_recommendations
from app.models import (
    RecommendationRequest,
    RecommendationResponse,
    FiltersResponse,
    HealthResponse,
    ErrorResponse,
)

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-load the dataset on server startup so the first request is fast."""
    logger.info("Starting up — pre-loading dataset...")
    load_data()
    logger.info("Dataset ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Zomato AI Restaurant Recommender API",
    description="Backend API for AI-powered restaurant recommendations using Groq LLM.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS ---
# Read allowed origins from env or fall back to defaults
allowed_origins_str = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes ---


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint for Railway deployment monitoring."""
    return HealthResponse(status="ok")


@app.get("/api/filters", response_model=FiltersResponse, tags=["Data"])
async def get_filters():
    """
    Return available filter options derived from the loaded dataset.

    Used by the frontend to populate dropdowns for location, cuisine,
    and to set the max value for the rating slider.
    """
    df = load_data()
    if df.empty:
        raise HTTPException(status_code=503, detail="Dataset unavailable.")

    filters = get_available_filters(df)
    return FiltersResponse(**filters)


@app.post(
    "/api/recommend",
    response_model=RecommendationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "No matching restaurants"},
        500: {"model": ErrorResponse, "description": "AI recommendation error"},
        503: {"model": ErrorResponse, "description": "Dataset or API unavailable"},
    },
    tags=["Recommendations"],
)
async def recommend(request: RecommendationRequest):
    """
    Generate AI-powered restaurant recommendations.

    1. Loads the cached dataset
    2. Filters by location, budget, rating, and cuisines
    3. Sends top 5 candidates to Groq LLM
    4. Returns ranked recommendations with personalized explanations
    """
    df = load_data()
    if df.empty:
        raise HTTPException(status_code=503, detail="Dataset unavailable.")

    # Step 1: Filter
    filtered_df = filter_restaurants(
        df,
        location=request.location,
        budget=request.budget,
        min_rating=request.min_rating,
        cuisines=request.cuisines if request.cuisines else None,
    )

    if filtered_df.empty:
        raise HTTPException(
            status_code=400,
            detail="No restaurants match your exact preferences. Try relaxing your filters!",
        )

    total_matches = len(filtered_df)
    top_candidates = filtered_df.head(5)
    candidates_analyzed = len(top_candidates)

    # Step 2: AI Recommendations
    try:
        recommendations = get_ai_recommendations(
            top_candidates,
            additional_preferences=request.additional_preferences,
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return RecommendationResponse(
        total_matches=total_matches,
        candidates_analyzed=candidates_analyzed,
        recommendations=recommendations,
    )
