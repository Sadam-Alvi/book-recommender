from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

df = pd.read_csv("dataset/books_cleaned.csv")

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

    book = df[df["book_id"] == book_id]

    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")

    book = book.iloc[0].to_dict()

    # Clean pages
    if pd.notna(book["num_pages"]):
        book["num_pages"] = str(book["num_pages"]).strip("[]'\"")

# Clean publication
    if pd.notna(book["publication"]):
        book["publication"] = str(book["publication"]).strip("[]'\"")

    return templates.TemplateResponse(
        request=request,
        name="book.html",
        context={
            "request": request,
            "book": book
        }
    )