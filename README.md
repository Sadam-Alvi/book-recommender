# Book Recommender

A Streamlit-based book recommendation app that serves fast, similarity-driven suggestions from a precomputed model. Users select a title and receive six related books with author names and cover images.

## Features
- Title selection from the full catalog
- Top-6 similarity recommendations
- Grid layout with cover images
- Fast inference using a precomputed sparse similarity matrix

## How It Works
The app loads:
- `Book_Details.csv` for metadata (title, author, cover URL)
- `similarity_matrix.pkl` for similarity scores
- `count_vectorizer.pkl` (loaded for completeness; not used at runtime in `display.py`)

When a user selects a book, the app finds its index, ranks similarity scores, and displays the top matches.

## Project Structure
- `display.py` — Streamlit app entry point
- `Book_Details.csv` — book metadata
- `similarity_matrix.pkl` — precomputed similarity matrix (required)
- `count_vectorizer.pkl` — serialized vectorizer (required by the current app)
- `app.ipynb` — notebook used to build or explore the model

## Requirements
- Python 3.9+
- `streamlit`
- `pandas`

## Quick Start
```bash
pip install streamlit pandas
streamlit run display.py
```

## Run the App
```bash
streamlit run display.py
```

Then open the local URL Streamlit prints in your terminal.

## Data Expectations
`Book_Details.csv` must include:
- `book_title`
- `author`
- `cover_image_uri`

## Notes
- If recommendations fail to load, verify that `similarity_matrix.pkl` and `count_vectorizer.pkl` are present in the project root.
- Cover images are loaded from the `cover_image_uri` column in `Book_Details.csv`.

## Troubleshooting
- Missing `*.pkl` files: regenerate or copy them into the project root.
- Broken images: confirm `cover_image_uri` values are valid URLs.

## License
Add your license here.
