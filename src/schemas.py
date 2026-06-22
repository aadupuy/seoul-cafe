from pydantic import BaseModel
from typing import Optional

# Define request and response models for the API
# The SearchRequest model includes the query, optional district, and top_k parameters for the search request.
class SearchRequest(BaseModel):
    query: str
    district: Optional[str] = None
    top_k: int = 5

# Define response model for the API
# The CafeRecommendation model represents a single cafe recommendation with its details and score.
class CafeRecommendation(BaseModel):
    name: str
    district: str
    category: str
    tags: str
    score: float

# The SearchResponse model includes the query, district, and a list of CafeRecommendation objects as results.
class SearchResponse(BaseModel):
    query: str
    district: Optional[str]
    results: list[CafeRecommendation]