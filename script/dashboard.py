import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = r'script\database\book_reviews.db'
conn = sqlite3.connect(DB_PATH)


# @st.cache_data
# def load_data():
#     df = pd.read_sql("SELECT * FROM books", conn)
#     return df


# df = load_data()

st.title("Book Reviewscope - Amazon Reviews")

# search for book
title = st.text_input("Search for book title", placeholder="Lord of the Rings")
search_params = (title,)
books = pd.read_sql(
    f"SELECT asin, title FROM books WHERE title LIKE '%{title}%' ORDER BY asin", conn
)
st.dataframe(books)

# # Kategorie-Filter
# kategorien = df["kategorie"].dropna().unique()
# kategorie_filter = st.multiselect("Kategorie auswählen", kategorien, default=kategorien)

# # Preisbereich-Filter
# min_preis = float(df["preis"].min())
# max_preis = float(df["preis"].max())
# preis_min, preis_max = st.slider(
#     "Preisbereich",
#     min_value=min_preis,
#     max_value=max_preis,
#     value=(min_preis, max_preis),
# )

# # Gefilterte Daten
# df_filtered = df[
#     (df["kategorie"].isin(kategorie_filter))
#     & (df["preis"] >= preis_min)
#     & (df["preis"] <= preis_max)
# ]

# st.subheader("Filtered Reviews")
# st.dataframe(df_filtered)
