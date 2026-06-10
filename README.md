# Seoul Cafe Recommender

A cafe recommendation system for Seoul built with Python.

The goal of this project is to recommend cafes based on user preferences such as atmosphere, location, and cafe characteristics.

This project is developed in stages:

- Week 1: Metadata-based filtering
- Week 2: Semantic search with embeddings
- Week 3: FastAPI backend
- Week 4: Docker containerization
- Week 5: Cloud deployment
- Week 6: Frontend and user interface

---

## Features

Current MVP supports:

- Cafe recommendations based on keywords
- District filtering
- Simple ranking based on matching tags
- Curated Seoul café dataset

Example queries:

```python
recommend(df, "dessert aesthetic")

recommend(df, "hanok cafe")

recommend(df, "work friendly", district="성수")
```

---

## Dataset

The current dataset contains 50 manually curated cafés from various districts in Seoul.

Available fields:

| Column   | Description                 |
| -------- | --------------------------- |
| name     | Cafe name                   |
| district | Seoul district/neighborhood |
| category | Café type                   |
| tags     | Descriptive attributes      |

Example:

| name | district | category | tags |
| --------- | ---- | ------------ | ----------------------- |
분카샤 을지로점 | 을지로 | dessert_cafe | dessert,aesthetic,photo |

Current tags include:
```bash
aesthetic
quiet
work_friendly
dessert
bakery
specialty_coffee
rooftop
brunch
vintage
minimal
large_space
date_spot
hanok
records
gallery
```

---

## Project Structure

```bash
seoul-cafe-recommender/
│
├── data/
│   ├── raw/
│   │   └── cafes_seed.csv
│   └── processed/
│
├── notebooks/
│   └── 01_mvp_filtering.ipynb
│
├── src/
│   └── recommender.py
│
├── README.md
└── requirements.txt
```

---

## Installation

```bash
git clone https://github.com/yourusername/seoul-cafe-recommender.git
cd seoul-cafe-recommender
pip install -r requirements.txt
```

---

## Usage

```python
import pandas as pd
from src.recommender import recommend

df = pd.read_csv("data/raw/cafes_seed.csv")
recommend(df, "quiet coffee")
```

Example output:

```bash
카페폴리
오디티
카페 다우드
더커피 성수
하우스오브바이닐 망원점
```

---

## Current Recommendation Logic

For each query:

1. User query is split into keywords
2. Keywords are matched against:
    * café name
    * district
    * category
    * tags
3. A match score is calculated
4. Results are ranked by score

---

## Limitations

Current version uses:

* Exact keyword matching
* Manually assigned tags
* Small curated dataset

This means the system does not yet understand semantic meaning.

For example:

```bash
quiet cafe
```

and 

```bash
good place to study
```

are treated as different queries even though they have similar intent.

---

## Future Improvements

Planned upgrades include:

* Sentence Transformer embeddings
* Semantic search
* FAISS vector database
* User review analysis
* FastAPI backend
* Docker deployment
* Cloud deployment (GCP Cloud Run)
* Web interface

---

## Tech Stack

* Python
* Pandas
* Jupyter Notebook

Planned:

* Sentence Transformers
* FAISS
* FastAPI
* Docker
* GCP Cloud Run

---

## Motivation

This project was inspired by a very simple problem: choosing a café.

As someone who enjoys café hopping in Seoul, I have hundreds of cafés saved across different neighborhoods. Many mornings I would open Kakao Maps or Naver Maps looking for a café that matched my mood for the day, only to spend a long time scrolling through my saved places, photos, and reviews.

I wanted a smarter way to search through cafés using natural language queries such as:

- "quiet café in Seongsu with good coffee"
- "aesthetic dessert café for a date"
- "minimal café to work from"

This project aims to turn that experience into a recommendation system that helps users discover cafés based on atmosphere and preferences rather than manually browsing maps.