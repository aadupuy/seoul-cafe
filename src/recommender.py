

def calculate_score(text, query_words):
    return sum(word in text for word in query_words)

def recommend(df, query, district=None, top_k=5):
    query_words = query.lower().split()
    results = df.copy()

    if district:
        results = results[results["district"].str.contains(district, case=False, na=False)]

    results["score"] = results["search_text"].apply(
        lambda text: calculate_score(text, query_words)
    )

    results = results[results["score"] > 0]
    return results.sort_values("score", ascending=False)[
        ["name", "district", "category", "tags", "score"]
    ].head(top_k)