import streamlit as st
from src.recommender import semantic_recommend

st.set_page_config(
    page_title="Seoul Cafe Recommender",
    page_icon="☕",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1000px;
        padding-top: 3rem;
    }

    h1 {
        font-size: 3rem !important;
    }

    h3 {
        font-size: 2rem !important;
    }

    label, p, div {
        font-size: 1.7rem !important;
    }

    .stTextInput input {
        font-size: 1.7rem !important;
        padding: 0.8rem !important;
    }

    .stButton button {
        font-size: 1.7rem !important;
        padding: 0.6rem 1.2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☕ Seoul Cafe Recommender")
st.write("Find cafés in Seoul based on your mood, location, and preferences.")

with st.container():
    query = st.text_input(
        "What kind of café are you looking for?",
        placeholder="quiet cafe with good coffee",
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        district = st.text_input(
            "District / neighborhood optional",
            placeholder="성수",
        )

    with col2:
        top_k = st.slider("Number", 1, 10, 5)

    st.caption(
        "Examples: quiet cafe in seongsu • date cafe in hongdae • specialty coffee • cozy dessert cafe"
    )

    search_clicked = st.button("Search")

if search_clicked:
    results = semantic_recommend(
        query=query,
        district=district if district.strip() else None,
        top_k=top_k,
    )

    st.subheader("Recommendations")

    for _, row in results.iterrows():
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.markdown(f"### ☕ {row['name']}")
                st.markdown(f"📍 **District:** {row['district']}")
                st.markdown(f"🏷️ **Tags:** {row['tags']}")

            with right:
                # st.metric("Score", f"{row['score']:.3f}")
                st.metric("Match", f"{row['score']:.0%}")