import pandas as pd 
import streamlit as st
import pickle
from importnb import Notebook
import nltk
import joblib
import os
df= pd.read_csv("Book_Details.csv")
df.dropna(inplace=True)



nltk.download("punkt")
nltk.download("punkt_tab")
@st.cache_data
def get_unique_values():
    return  df["book_title"].dropna().unique().tolist()
books = get_unique_values()

with open('similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)




book_index = {book: i for i, book in enumerate(df['book_title'])}

def recommend(book_title, top_n=6):
    # Check if book exists
    idx = book_index.get(book_title)
    if idx is None:
        return f"Book '{book_title}' not found."

    # ----- Get similarity scores -----
    # Works for both dense and sparse matrix
    if hasattr(similarity_matrix, "getrow"):          # sparse
        row = similarity_matrix.getrow(idx)
        sim_scores = list(zip(row.indices, row.data))
    else:                                             # dense
        sim_scores = list(enumerate(similarity_matrix[idx]))

    # Sort by similarity (highest first) and skip itself
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Remove the book itself (similarity = 1.0)
    sim_scores = [score for score in sim_scores if score[0] != idx][:top_n]

    # Get book indices
    book_indices = [i[0] for i in sim_scores]

    # Return the selected columns
    return df[['book_title', 'author', 'cover_image_uri', 'book_details','authorlink']].iloc[book_indices].values.tolist()



book = st.selectbox(
    "Select a Book",
    books
)



if st.button("Recommend Similar Books"):

    recommended_books = recommend(book)

    cols = st.columns(3)

    for idx, (title, author, img, details, author_link) in enumerate(recommended_books):

        with cols[idx % 3]:

            # Book title
            st.markdown(f"**{title}**")

            # Clickable author name
            if author_link:
                st.markdown(
                    f'<a href="{author_link}" target="_blank">{author}</a>',
                    unsafe_allow_html=True
                    )
            else:
                st.write(author)

            # Book image
            st.image(img, use_container_width=True)

            # Clickable details section
            with st.expander("📖 View Details"):
                st.write(details)

        # Create a new row after every 3 books
        if (idx + 1) % 3 == 0:
            cols = st.columns(3)
