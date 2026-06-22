import pandas as pd
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


DATA_PATH = "data/processed/cafes_with_search_text.csv"
EMBEDDINGS_PATH = "data/processed/cafe_embeddings.npy"
INDEX_PATH = "data/processed/cafe_faiss.index"


df = pd.read_csv(DATA_PATH)
embeddings = np.load(EMBEDDINGS_PATH)
index = faiss.read_index(INDEX_PATH)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def semantic_recommend(query, top_k=5, district=None):
    results_df = df.copy()

    if district:
        mask = results_df["district"].str.contains(
            district,
            case=False,
            na=False,
        )
        candidate_indices = results_df[mask].index.tolist()
    else:
        candidate_indices = results_df.index.tolist()

    if not candidate_indices:
        return pd.DataFrame(
            columns=["name", "district", "category", "tags", "score"]
        )

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    scores, indices = index.search(query_embedding, len(df))

    recommendations = []

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

        if len(recommendations) >= top_k:
            break

    return pd.DataFrame(recommendations)