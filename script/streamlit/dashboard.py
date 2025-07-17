import streamlit as st
import pandas as pd
import sqlite3
import os
from functools import partial
import psycopg2


@st.cache_data
def get_data(query="SELECT * FROM books;", search_params=()):
    """
    connect to database and get data
    search_params should be used as a tuple to avoid SQL Injection when user input is incorporated in a query
    """
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
    )
    df = pd.read_sql_query(query, conn, params=search_params)

    conn.close()
    return df


st.title("Book Reviewscope - Amazon Reviews")
# Filter database with various parameters
st.subheader("Filter results")
# Filters
asin_choice = st.text_input("asin", key=ELEMENT_KEYS["asin"])

filtered_results = st.container()
# Searching for books in the database to get asin
st.subheader("Book Search")

title_search = st.text_input(
    "Search for book title",
    placeholder="Lord of the Rings",
)
search_results = st.container()

# collect all the filters and create a query which is then applied to the dataframe

query_conditions = ""
params = []
if asin_choice:
    query_conditions += "AND B.asin=%s "
    params.append(asin_choice)

complete_query = f"SELECT B.title, B.genre, R.rating, R.summary, S.phrase, S.polarity, B.price FROM books as B, reviews as R, sentiments as S WHERE B.asin = R.asin AND R.id = S.review_id {query_conditions}ORDER BY B.asin LIMIT 1000"
filtered = get_data(query=complete_query, search_params=params)
with filtered_results:
    st.write(complete_query, params)
    st.dataframe(filtered)

# TODO Author search, full text search, minimizable
# search for books and return the asin
if title_search:
    query = f"SELECT asin, title FROM books WHERE title LIKE %s ORDER BY asin"
    params = (f"%{title_search}%",)
    books = get_data(query=query, search_params=params)
    with search_results:
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
