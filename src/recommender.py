import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# Define paths for data and model files
DATA_PATH = "data/processed/cafes_with_search_text.csv"
EMBEDDINGS_PATH = "data/processed/cafe_embeddings.npy"
INDEX_PATH = "data/processed/cafe_faiss.index"

# Load the dataset, embeddings, and FAISS index
df = pd.read_csv(DATA_PATH)
embeddings = np.load(EMBEDDINGS_PATH)
index = faiss.read_index(INDEX_PATH)

# Load the pre-trained SentenceTransformer model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Define the semantic recommendation function
# This function takes a query, top_k, and district as input and returns a DataFrame of recommended cafes.
def semantic_recommend(query, top_k=5, district=None):
    results_df = df.copy()

    # Filter the results based on the district if provided
    if district:
        mask = results_df["district"].str.contains(
            district,
            case=False,
            na=False,
        )
        candidate_indices = results_df[mask].index.tolist()
    else: # If no district is provided, consider all cafes as candidates
        candidate_indices = results_df.index.tolist()

    if not candidate_indices: # If no candidates are found after filtering, return an empty DataFrame with the specified columns
        return pd.DataFrame(
            columns=["name", "district", "category", "tags", "score"]
        )

    # Encode the query using the SentenceTransformer model to obtain its embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Perform a search in the FAISS index using the query embedding to retrieve scores and indices of the most similar cafes
    scores, indices = index.search(query_embedding, len(df))

    recommendations = []

    # Iterate through the scores and indices, and for each index that is in the candidate_indices, 
    # append the corresponding cafe information to the recommendations list
    for score, idx in zip(scores[0], indices[0]):
        if idx in candidate_indices:
            recommendations.append(
                {
                    "name": df.iloc[idx]["name"],
                    "district": df.iloc[idx]["district"],
                    "category": df.iloc[idx]["category"],
                    "tags": df.iloc[idx]["tags"],
                    "score": float(score),
                }
            )

        if len(recommendations) >= top_k: # If the number of recommendations reaches top_k, stop the iteration
            break

    return pd.DataFrame(recommendations)