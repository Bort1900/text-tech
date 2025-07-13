import streamlit as st
import pandas as pd
import sqlite3
import os
from functools import partial


# def book_search(param):
#     print("hey")
#     print(param)
#     search_params = (title,)
#     books = pd.read_sql_query(
#         f"SELECT asin, title FROM books WHERE title LIKE '%{title}%' ORDER BY asin",
#         conn,
#     )
#     st.dataframe(books)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database/book_reviews.db")
st.write(db_path)
# conn = sqlite3.connect(db_path)


# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())

# @st.cache_data
# def load_data():
#     df = pd.read_sql("SELECT * FROM books", conn)
#     return df


# df = load_data()

st.title("Book Reviewscope - Amazon Reviews")

# search for book
# title = st.text_input(
#     "Search for book title",
#     placeholder="Lord of the Rings",
#     value="ses",
#     on_change=book_search,
# )


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
