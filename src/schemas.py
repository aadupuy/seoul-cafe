from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: str
    district: Optional[str] = None
    top_k: int = 5


class CafeRecommendation(BaseModel):
    name: str
    district: str
    category: str
    tags: str
    score: float


class SearchResponse(BaseModel):
    query: str
    district: Optional[str]
    results: list[CafeRecommendation]