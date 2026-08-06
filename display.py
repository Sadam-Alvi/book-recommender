import pandas as pd 
import streamlit as st
import pickle
from importnb import Notebook



df= pd.read_csv("Book_Details.csv")
df.dropna(inplace=True)





with Notebook():
    import app   # without the .ipynb extension

# Now the similarity matrix is available
similarity_matrix = app.similarity_matrix   

with open('count_vectorizer.pkl', 'rb') as f:
    cv = pickle.load(f)


movie_index = {book: i for i, book in enumerate(df['book_title'])}

def recommend(book_title, top_n=6):
    # Check if movie exists
    idx = movie_index.get(book_title)
    if idx is None:
        return f"Movie '{book_title}' not found."

    # Get similarity scores for this movie
    sim_scores = list(enumerate(similarity_matrix[idx].toarray()[0]))  # convert sparse row to array

    # Sort by similarity (highest first) and skip itself
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    # Get movie indices
    book_indices = [i[0] for i in sim_scores]

    # Return movie names
    return df[['book_title','author','cover_image_uri']].iloc[book_indices].values.tolist()



book = st.selectbox(
    "Select a Book",
    df["book_title"].tolist()
)




if st.button("Recommend Similar books"):

    recommended_books = recommend(book)

    cols = st.columns(3)   # 3 columns per row

    for idx, (title, author, img) in enumerate(recommended_books):

        with cols[idx % 3]:   # Move across 3 columns
            st.text(f"{title} by {author}")
            st.image(img, use_container_width=True)

        # After every 3 books, create a new row
        if (idx + 1) % 3 == 0:
            cols = st.columns(3)
