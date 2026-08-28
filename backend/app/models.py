from pydantic import BaseModel, Field
from typing import Optional


class RecommendationRequest(BaseModel):
    """Request body for the /api/recommend endpoint."""
    location: str = Field(default="Any", description="Restaurant location filter")
    budget: str = Field(default="Any", description="Budget category: Any, Low, Medium, or High")
    min_rating: float = Field(default=3.5, ge=0.0, le=5.0, description="Minimum restaurant rating")
    cuisines: list[str] = Field(default_factory=list, description="List of preferred cuisines")
    additional_preferences: str = Field(default="", description="Free-text additional preferences")


class RecommendationItem(BaseModel):
    """A single restaurant recommendation from the AI."""
    name: str
    rating: Optional[float] = None
    cost: Optional[str] = None
    cuisines: Optional[str] = None
    explanation: str = "No explanation provided."


class RecommendationResponse(BaseModel):
    """Response body for the /api/recommend endpoint."""
    total_matches: int
    candidates_analyzed: int
    recommendations: list[RecommendationItem]


class FiltersResponse(BaseModel):
    """Response body for the /api/filters endpoint."""
    locations: list[str]
    cuisines: list[str]
    max_rating: float


class HealthResponse(BaseModel):
    """Response body for the /api/health endpoint."""
    status: str = "ok"


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
