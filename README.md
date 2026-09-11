# 📚 Book Recommender System

A content-based book recommendation system that helps users discover similar books based on their **title, author, genres, and book description**.

The project uses **TF-IDF vectorization** and **cosine similarity** to represent books and identify the most similar titles. A FastAPI web application provides a clean interface for browsing books, viewing details, and discovering similar recommendations.

---

## 📖 Project Overview

This project combines **Natural Language Processing (NLP), machine learning, and web development** to build a book discovery platform.

Each book is represented using important textual features such as:

* Book title
* Author
* Genres
* Book description

These features are combined and transformed into numerical vectors using **TF-IDF**. The system then uses cosine similarity to identify books with similar content.

The recommendation results are precomputed and stored so that recommendations can be retrieved quickly when a user opens a book.

---

## ✨ Key Features

* 🔎 **Book Search** – Search books by title.
* 📚 **Genre Filtering** – Filter books by genre.
* 📖 **Book Details** – View information about a selected book.
* 🤖 **Content-Based Recommendations** – Find books similar to the selected book.
* ⚡ **Fast Recommendations** – The top similar books are precomputed instead of calculating similarities for every request.
* 🖼️ **Book Covers** – Display book cover images in a responsive grid.
* 👤 **Author Information** – Display author information and author profiles when available.
* ⭐ **Ratings** – Show average book ratings.
* 📱 **Responsive UI** – Book cards adapt to different screen sizes.

---

## 🧠 How the Recommendation System Works

### 1. Data Preparation

The book dataset is loaded using Pandas.

Relevant features are cleaned and combined into a single text representation.

Example:

```text
title + author + genres + book description
```

This combined representation is used as the input for the recommendation model.

---

### 2. TF-IDF Vectorization

The combined book information is converted into numerical vectors using:

```python
TfidfVectorizer()
```

TF-IDF assigns importance to words based on how frequently they occur in a book's information while reducing the importance of words that occur across many books.

Each book is therefore represented as a vector in a high-dimensional feature space.

---

### 3. Cosine Similarity

Cosine similarity measures how similar two book vectors are.

The formula is:

```text
Similarity(A, B) = (A · B) / (||A|| ||B||)
```

A higher cosine similarity means that the books have more similar textual features.

---

### 4. Nearest-Neighbor Recommendation

Instead of creating a complete similarity matrix containing every book-to-book comparison, the system uses:

```python
NearestNeighbors(
    n_neighbors=21,
    metric="cosine",
    algorithm="brute"
)
```

The first result is the book itself, so it is removed.

The remaining results provide the **20 most similar books** for every book in the dataset.

This approach significantly reduces the amount of similarity information that needs to be stored.

---

### 5. Precomputed Recommendations

The recommendation indices and similarity scores are saved using Pickle:

```python
recommendation_data = {
    "indices": similarity_indices,
    "scores": similarity_scores
}
```

This is stored in:

```text
book_similarity.pkl
```

When a user opens a book, FastAPI retrieves the precomputed recommendations instead of recalculating similarities.

---

## 🏗️ Application Architecture

```text
                    Book Dataset
                         │
                         ▼
                Data Preprocessing
                         │
                         ▼
              Feature Combination
        Title + Author + Genre + Description
                         │
                         ▼
                 TF-IDF Vectorizer
                         │
                         ▼
              Book Feature Matrix
                         │
                         ▼
              NearestNeighbors
                         │
                         ▼
              Top 20 Similar Books
                         │
                         ▼
               book_similarity.pkl
                         │
                         ▼
                    FastAPI
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Search / Genre           Book Details
                                     │
                                     ▼
                              Similar Books
                                     │
                                     ▼
                               HTML + CSS
```

---

## 📁 Project Structure

```text
book-recommender/
│
├── dataset/
│   ├── books_cleaned.csv
│   └── book_similarity.pkl
│
├── templates/
│   ├── index.html
│   └── book.html
│
├── static/
│   └── style.css
│
├── main.py
├── app.ipynb
├── requirements.txt
└── README.md
```

### File Description

| File                  | Description                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| `app.ipynb`           | Data preprocessing, TF-IDF vectorization, and recommendation generation |
| `main.py`             | FastAPI backend and application routes                                  |
| `books_cleaned.csv`   | Cleaned book dataset                                                    |
| `book_similarity.pkl` | Precomputed top-20 similar books and similarity scores                  |
| `index.html`          | Homepage, search, genre filtering, and book grid                        |
| `book.html`           | Individual book details and similar books                               |
| `style.css`           | Website styling and responsive layout                                   |
| `requirements.txt`    | Python dependencies                                                     |

---

## 🛠️ Technologies Used

### Machine Learning / NLP

* **Python**
* **Pandas**
* **Scikit-learn**
* **TF-IDF**
* **Cosine Similarity**
* **NearestNeighbors**
* **Pickle**

### Web Development

* **FastAPI**
* **Jinja2**
* **HTML**
* **CSS**
* **Uvicorn**

---

## 📊 Dataset

The cleaned dataset contains information about books and their metadata.

Important columns include:

| Column             | Description                        |
| ------------------ | ---------------------------------- |
| `book_id`          | Unique identifier for each book    |
| `book_title`       | Title of the book                  |
| `author`           | Author name                        |
| `genres`           | Book genre/categories              |
| `book_details`     | Description or summary of the book |
| `average_rating`   | Average book rating                |
| `num_pages`        | Number of pages                    |
| `publication_info` | Publication information            |
| `cover_image_uri`  | URL of the book cover              |
| `authorlink`       | Author profile URL, when available |

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Sadam-Alvi/book-recommender.git
cd book-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Generate Recommendations

Run the Jupyter notebook:

```bash
jupyter notebook app.ipynb
```

The notebook performs:

1. Data loading
2. Data cleaning
3. Text preprocessing
4. Feature combination
5. TF-IDF vectorization
6. Nearest-neighbor calculation
7. Saving recommendation data

The generated recommendation file is:

```text
book_similarity.pkl
```

---

### 4. Start the FastAPI Server

Run:

```bash
python -m uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## 🌐 Application Pages

### Homepage

The homepage allows users to:

* Search for a book
* Filter books by genre
* Browse the book collection
* Open a book to view more information

Each book is displayed as a card containing:

* Cover
* Title
* Author
* Rating

---

### Book Details Page

When a user selects a book, the application displays information such as:

* Book cover
* Title
* Author
* Rating
* Number of pages
* Publication information
* Description

Below the selected book, the application displays the **20 most similar books**.

Users can click any recommended book to open its details page.

---

## 🔄 Recommendation Flow

When a user opens a book:

```text
User selects a book
        ↓
FastAPI receives book_id
        ↓
Find book in dataset
        ↓
Get its row position
        ↓
Retrieve precomputed recommendation indices
        ↓
Retrieve similarity scores
        ↓
Get corresponding books from dataset
        ↓
Display similar books
```

Because recommendations are precomputed, the application does not need to calculate the similarity between all books during every user request.

---

## ⚙️ Recommendation Storage

The recommendation model stores two arrays:

```python
{
    "indices": similarity_indices,
    "scores": similarity_scores
}
```

### `indices`

Contains the row positions of the most similar books.

Example:

```text
Book 0 → [15, 82, 134, 421, ...]
```

### `scores`

Contains the corresponding similarity scores:

```text
Book 0 → [0.82, 0.76, 0.71, 0.68, ...]
```

The first nearest neighbor is the book itself, so it is excluded before storing the final recommendations.

---

## 🚀 Performance

The recommendation system uses precomputed nearest neighbors to avoid repeatedly calculating book-to-book similarity during user requests.

Instead of storing a complete:

```text
N × N
```

similarity matrix, the system stores only the top 20 recommendations for each book.

For example, with 16,225 books:

```text
Full similarity matrix:

16,225 × 16,225
```

would require hundreds of millions of similarity values.

The top-20 approach stores approximately:

```text
16,225 × 20
```

recommendation indices and scores.

This makes the recommendation data substantially more manageable while still providing useful recommendations.

---

## 🎯 How to Use

### Step 1 — Search

Enter a book title into the search field.

### Step 2 — Filter

Optionally select a genre.

### Step 3 — Open a Book

Click a book card to view its details.

### Step 4 — Explore Recommendations

Scroll down to:

```text
Similar Books
```

The system displays the top 20 books identified as most similar to the selected book.

### Step 5 — Continue Exploring

Click any recommended book to view its details and its own recommendations.

---

## 🔧 Troubleshooting

| Problem                            | Possible Solution                                                                 |
| ---------------------------------- | --------------------------------------------------------------------------------- |
| `book_similarity.pkl` not found    | Run `app.ipynb` to generate the recommendation file                               |
| `pickle` is not defined            | Add `import pickle` to `main.py`                                                  |
| Book not found                     | Check the `book_id` in the dataset                                                |
| Recommendations cause `IndexError` | Ensure the pickle was generated from the same dataset currently loaded by FastAPI |
| Book covers do not load            | Check the `cover_image_uri` values                                                |
| Search returns no results          | Check the spelling of the book title                                              |
| Recommendations seem irrelevant    | Improve text preprocessing or feature weighting                                   |
| Application does not start         | Check dependencies and run Uvicorn using `python -m uvicorn main:app --reload`    |

---

## ⚠️ Important Dataset Requirement

The `book_similarity.pkl` file must be generated using the **same dataset and row ordering** used by FastAPI.

For example:

```python
df = pd.read_csv("dataset/books_cleaned.csv")
df = df.reset_index(drop=True)

df["book_id"] = range(len(df))
```

The dataframe should not be reordered after generating the recommendation indices.

Otherwise, recommendation indices may point to the wrong books or cause:

```text
IndexError: positional indexers are out-of-bounds
```

---

## 🔮 Future Improvements

Possible improvements include:

* 🔹 Semantic embeddings using Sentence Transformers
* 🔹 Better feature weighting between author, title, genre, and description
* 🔹 Hybrid recommendation using ratings and content similarity
* 🔹 Personalized recommendations based on user history
* 🔹 Recommendation explanations such as "Similar because of genre and author"
* 🔹 Improved duplicate-book handling
* 🔹 Pagination for large book collections
* 🔹 Advanced search by author and genre
* 🔹 User accounts and saved books
* 🔹 Recommendation evaluation using Precision@K, Recall@K, and NDCG

---

## 📌 Limitations

This is currently a **content-based recommendation system**.

Recommendations depend on the information available in the dataset. Books with incomplete descriptions, missing genres, or limited metadata may produce weaker recommendations.

The system also does not currently learn from individual user preferences or reading history.

---

## 🎓 Concepts Demonstrated

This project demonstrates practical knowledge of:

* Data cleaning with Pandas
* NLP preprocessing
* TF-IDF vectorization
* Vector-space representations
* Cosine similarity
* Nearest-neighbor search
* Recommendation systems
* Model/data serialization with Pickle
* FastAPI backend development
* Jinja2 templates
* HTML/CSS frontend development
* REST-style application routing
* Responsive web design

---

## 👨‍💻 Author

**Sadam Alvi**

GitHub: [Sadam-Alvi](https://github.com/Sadam-Alvi)

---

## 📄 License

This project is intended for educational and portfolio purposes.
