import streamlit as st
import pandas as pd
import sqlite3
import os
from functools import partial
import psycopg2

st.title("Book Reviewscope - Amazon Reviews")


@st.cache_data
def get_data(query="SELECT * FROM books;"):
    """
    connect to database and get data
    """
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
    )
    df = pd.read_sql_query(query, conn)

    conn.close()
    return df
st.subheader("Book Search")


def book_search(key):
    '''
        returns the results for books as specified in the object value of the key object
    '''
    title = st.session_state["key"]
    query= f"SELECT asin, title FROM books WHERE title LIKE '%{title}%' ORDER BY asin"
    books = get_data(query=query)
    st.dataframe(books)


# search for book in database to get asin
title = st.text_input(
    "Search for book title",
    placeholder="Lord of the Rings",
    key ="book_search",
    value="Lord",
    on_change=partial(book_search,"book_search")
)

# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())

# @st.cache_data
# def load_data():
#     df = pd.read_sql("SELECT * FROM books", conn)
#     return df


# df = load_data()


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
