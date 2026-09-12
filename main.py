from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import ast

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# -------------------------
# LOAD DATA
# -------------------------

df = pd.read_csv("dataset/Book_Details.csv")


# -------------------------
# EXTRACT PUBLICATION YEAR
# -------------------------

df["year"] = (
    df["publication_info"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
)


# -------------------------
# PROCESS GENRES
# -------------------------

def get_genres(value):

    try:
        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    except:
        return []


df["genre_list"] = df["genres"].apply(get_genres)


# -------------------------
# FIND TOP 20 GENRES
# -------------------------

genre_counts = {}

for genres in df["genre_list"]:

    for genre in genres:

        genre_counts[genre] = (
            genre_counts.get(genre, 0) + 1
        )


top_20_genres = sorted(
    genre_counts,
    key=genre_counts.get,
    reverse=True
)[:20]


# -------------------------
# AUTHOR SUGGESTIONS
# -------------------------

authors = (
    df["author"]
    .dropna()
    .drop_duplicates()
    .astype(str)
    .str.strip()
)

all_authors = authors[authors != ""]




# -------------------------
# PUBLICATION YEARS
# -------------------------

years = (
    df["year"]
    .dropna()
    .astype(int)
    .unique()
)

years = sorted(years)
@app.get("/")
def home(
    request: Request,
    selected_genres: list[str] | None = None,
    author: str = "",
    year: int | None = None
):
    # Maximum 3 genres
    selected_genres = (selected_genres or [])[:3]

    # Start with no filters
    filtered_df = df.copy()

    # Check whether user submitted any preference
    has_preferences = (
        bool(selected_genres)
        or bool(author.strip())
        or year is not None
    )

    if has_preferences:

        # -------------------------
        # GENRE MATCH
        # -------------------------

        if selected_genres:

            genre_match = df["genre_list"].apply(
                lambda genres: any(
                    genre in genres
                    for genre in selected_genres
                )
            )

        else:
            genre_match = pd.Series(
                False,
                index=df.index
            )


        # -------------------------
        # AUTHOR MATCH
        # -------------------------

        if author.strip():

            author_match = (
                df["author"]
                .fillna("")
                .str.lower()
                .str.strip()
                == author.strip().lower()
            )

        else:
            author_match = pd.Series(
                False,
                index=df.index
            )


        # -------------------------
        # YEAR MATCH
        # -------------------------

        if year is not None:

            year_match = (
                df["year"] == year
            )

        else:
            year_match = pd.Series(
                False,
                index=df.index
            )


        # -------------------------
        # ANY PREFERENCE MATCH
        # -------------------------

        final_match = (
            genre_match
            | author_match
            | year_match
        )

        filtered_df = df[final_match].copy()


        # -------------------------
        # CONVERT REVIEWS/RATING
        # -------------------------

        filtered_df["num_reviews"] = pd.to_numeric(
            filtered_df["num_reviews"],
            errors="coerce"
        ).fillna(0)

        filtered_df["average_rating"] = pd.to_numeric(
            filtered_df["average_rating"],
            errors="coerce"
        ).fillna(0)


        # -------------------------
        # SORT BOOKS
        # -------------------------

        filtered_df = filtered_df.sort_values(
            by=["num_reviews", "average_rating"],
            ascending=[False, False]
        )


    # -------------------------
    # BOOK DATA FOR TEMPLATE
    # -------------------------

    books = filtered_df.to_dict(
        orient="records"
    )


    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "books": books,

            "selected_genres": selected_genres,

            "author": author,

            "year": year,

            "top_20_genres": top_20_genres,

            "all_authors": all_authors,

            "years": years
        }
    )

@app.get("/results")
def results(
    request: Request,
    selected_genres: list[str] | None = None,
    author: str = "",
    year: int | None = None
):

    selected_genres = (selected_genres or [])[:3]
    author = author.strip()

    # -------------------------
    # CHECK PREFERENCES
    # -------------------------

    if not selected_genres and not author and year is None:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "top_20_genres": top_20_genres,
                "all_authors": all_authors,
                "years": years,
                "error": "Please select at least one preference."
            }
        )

    books_df = df.copy()

    # -------------------------
    # CONVERT NUMERIC COLUMNS
    # -------------------------

    books_df["average_rating"] = pd.to_numeric(
        books_df["average_rating"],
        errors="coerce"
    ).fillna(0)

    books_df["num_reviews"] = pd.to_numeric(
        books_df["num_reviews"],
        errors="coerce"
    ).fillna(0)

    books_df["preference_score"] = 0.0

    # -------------------------
    # AUTHOR PREFERENCE
    # -------------------------

    if author:

        author_match = (
            books_df["author"]
            .fillna("")
            .str.strip()
            .str.lower()
            == author.lower()
        )

        books_df.loc[
            author_match,
            "preference_score"
        ] += 5

    # -------------------------
    # GENRE PREFERENCE
    # -------------------------

    if selected_genres:

        def genre_score(genres):

            matches = sum(
                genre in genres
                for genre in selected_genres
            )

            return matches * 3

        books_df["preference_score"] += (
            books_df["genre_list"]
            .apply(genre_score)
        )

    # -------------------------
    # YEAR PREFERENCE
    # -------------------------

    if year is not None:

        year_match = books_df["year"] == year

        books_df.loc[
            year_match,
            "preference_score"
        ] += 3

    # -------------------------
    # NORMALIZE REVIEWS
    # -------------------------

    max_reviews = books_df["num_reviews"].max()

    if max_reviews > 0:
        books_df["review_score"] = (
            books_df["num_reviews"] / max_reviews
        )
    else:
        books_df["review_score"] = 0

    # -------------------------
    # FINAL SCORE
    # -------------------------

    books_df["final_score"] = (
        books_df["preference_score"] * 10
        + books_df["average_rating"] * 2
        + books_df["review_score"] * 2
    )

    # -------------------------
    # SORT BY SCORE
    # -------------------------

    books_df = books_df.sort_values(
        by="final_score",
        ascending=False
    )

    # -------------------------
    # REMOVE DUPLICATE BOOKS
    # -------------------------

    books_df["title_key"] = (
        books_df["book_title"]
        .fillna("")
        .str.strip()
        .str.lower()
    )

    books_df = books_df.drop_duplicates(
        subset="title_key",
        keep="first"
    )

    # Remove temporary column
    books_df = books_df.drop(
        columns=["title_key"]
    )

    # -------------------------
    # LIMIT RESULTS
    # -------------------------

    books_df = books_df.head(100)

    # -------------------------
    # CONVERT TO DICTIONARY
    # -------------------------

    books = books_df.to_dict(
        orient="records"
    )

    # -------------------------
    # RESULTS PAGE
    # -------------------------

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "books": books,
            "selected_genres": selected_genres,
            "author": author,
            "year": year
        }
    )
@app.get("/book/{book_id}")
def book_details(request: Request, book_id: int):

    # Find selected book
    book_df = df[df["book_id"] == book_id]

    if book_df.empty:
        return {"error": "Book not found"}

    # Convert selected book to dictionary
    book = book_df.iloc[0].to_dict()

    # -------------------------
    # FIND SIMILAR BOOKS
    # -------------------------

    # Books with same author
    similar_df = df[
        (df["author"] == book["author"]) &
        (df["book_id"] != book_id)
    ].copy()

    # If not enough books, add books from same genre
    if len(similar_df) < 10:

        genre_list = get_genres(book["genres"])

        genre_books = df[
            df["genre_list"].apply(
                lambda genres: any(
                    genre in genres
                    for genre in genre_list
                )
            )
            & (df["book_id"] != book_id)
        ]

        similar_df = pd.concat(
            [similar_df, genre_books]
        ).drop_duplicates(
            subset="book_id"
        )

    # Sort by rating
    similar_df["average_rating"] = pd.to_numeric(
        similar_df["average_rating"],
        errors="coerce"
    ).fillna(0)

    similar_df = similar_df.sort_values(
        by="average_rating",
        ascending=False
    ).head(10)

    similar_books = similar_df.to_dict(
        orient="records"
    )

    # -------------------------
    # RENDER PAGE
    # -------------------------

    return templates.TemplateResponse(
        request=request,
        name="book.html",
        context={
            "book": book,
            "similar_books": similar_books
        }
    )