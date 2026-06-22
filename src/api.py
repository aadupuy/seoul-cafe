from fastapi import FastAPI, HTTPException
from src.schemas import SearchRequest, SearchResponse
from src.recommender import semantic_recommend

# Initialize the FastAPI app
app = FastAPI(
    title="Seoul Cafe Recommender API", # Title for the API
    description="Semantic café recommendation API using Sentence Transformers and FAISS.", # Description for the API
    version="0.1.0", # Version of the API
)

# Define the root endpoint
@app.get("/") 
def root():
    return {"message": "Seoul Cafe Recommender API is running"} # Return a simple message indicating the API is running

# Define the health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Define the search endpoint
# This endpoint accepts a POST request with a SearchRequest payload and returns a SearchResponse.
@app.post("/search", response_model=SearchResponse) # Define the POST endpoint for searching cafes
def search(request: SearchRequest): 
    if not request.query.strip(): # Check if the query is empty or contains only whitespace
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    if request.top_k < 1 or request.top_k > 20: # Check if the top_k parameter is within the valid range (1 to 20)
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 20.")

    # Perform semantic recommendation using the provided query, district, and top_k parameters
    results = semantic_recommend(
        query=request.query,
        district=request.district,
        top_k=request.top_k,
    )

    # Return the search results in the specified format
    return {
        "query": request.query,
        "district": request.district,
        "results": results.to_dict(orient="records"),
    }