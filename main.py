from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import pickle
app = FastAPI()

df = pd.read_csv("dataset/Book_Details.csv")
with open("matrix/book_similarity.pkl", "rb") as f:
    recommendation_data = pickle.load(f)

similarity_indices = recommendation_data["indices"]
similarity_scores = recommendation_data["scores"]
import ast

def process_genres(x):
    if pd.isna(x):
        return ""
    
    if isinstance(x, list):
        return " ".join(x)
    
    try:
        x = ast.literal_eval(x)
        return " ".join(x) if isinstance(x, list) else str(x)
    except:
        return str(x)

df['genres'] = df['genres'].apply(process_genres)
# Create an ID if your dataset doesn't already have one
if "book_id" not in df.columns:
    df["book_id"] = range(len(df))

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(
    request: Request,
    search: str = "",
    genre: str = ""
):

    filtered_df = df.copy()

    # Search
    if search:
        filtered_df = filtered_df[
            filtered_df["book_title"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    # Genre filter
    if genre:
        filtered_df = filtered_df[
            filtered_df["genres"]
            .astype(str)
            .str.contains(genre, case=False, na=False)
        ]

    books = filtered_df.iloc[:200].to_dict("records")

    genres = sorted(
        set(
            g.strip()
            for value in df["genres"].dropna()
            for g in str(value).split(",")
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "books": books,
            "genres": genres,
            "search": search,
            "genre": genre
        }
    )


# BOOK DETAILS PAGE
@app.get("/book/{book_id}")
def book_details(request: Request, book_id: int):

    # Find selected book
    book = df[df["book_id"] == book_id]

    if book.empty:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Get row index
    book_index = book.index[0]

    # Selected book details
    book = book.iloc[0].to_dict()

    # Clean pages
    if pd.notna(book["num_pages"]):
        book["num_pages"] = str(
            book["num_pages"]
        ).strip("[]'\"")

    # Clean publication
    if pd.notna(book["publication_info"]):
        book["publication_info"] = str(
            book["publication_info"]
        ).strip("[]'\"")

    # -----------------------------
    # Similar books
    # -----------------------------

    similar_indices = similarity_indices[book_index]
    similar_scores = similarity_scores[book_index]

    similar_books = df.iloc[similar_indices].copy()

    similar_books["similarity"] = similar_scores

    similar_books = similar_books.to_dict("records")

    return templates.TemplateResponse(
        request=request,
        name="book.html",
        context={
            "request": request,
            "book": book,
            "similar_books": similar_books
        }
    )