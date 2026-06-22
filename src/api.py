from fastapi import FastAPI, HTTPException
from src.schemas import SearchRequest, SearchResponse
from src.recommender import semantic_recommend

app = FastAPI(
    title="Seoul Cafe Recommender API",
    description="Semantic café recommendation API using Sentence Transformers and FAISS.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Seoul Cafe Recommender API is running"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if request.top_k < 1 or request.top_k > 20:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 20.")

    results = semantic_recommend(
        query=request.query,
        district=request.district,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "district": request.district,
        "results": results.to_dict(orient="records"),
    }