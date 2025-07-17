import streamlit as st
import pandas as pd
from functools import partial
import psycopg2
from streamlit_tags import st_tags


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


@st.cache_data
def get_genres():
    query = "SELECT genre FROM books GROUP BY genre"
    genres = get_data(query=query)
    return list(genres["genre"])


def get_disjunction_query(column, element):
    """
    returns query for a disjunction
    """
    conditions += f"AND {column} IN ("
    for i in range(len(element)):
        if i > 0:
            conditions += "%s"
    conditions += ") "
    return conditions


st.title("Book Reviewscope - Amazon Reviews")
# Filter database with various parameters
st.subheader("Filter results")
# Filters
# TODO text searches
asin_choice = st.text_input("asin")
keyword_choice = st_tags(
    label="Keywords:",
    text="Press enter to add more",
)

rating_choice = st.slider("Rating", min_value=1, max_value=5, value=(1, 5))
price_choice = st.slider(
    "Price", min_value=0, max_value=100, format="%0.2f", value=(1, 10)
)
genre_choice = st.multiselect("Genres", get_genres())


filtered_results = st.container()
# Searching for books in the database to get asin
st.subheader("Book Search")

title_search = st.text_input(
    "Search for book title",
    placeholder="Hamlet",
)
author_search = st.text_input(
    "Search for author",
    placeholder="Shakespeare",
)
search_results = st.container()

# collect all the filters and create a query which is then applied to the dataframe

query_conditions = ""
params = []
if asin_choice:
    query_conditions += "AND B.asin=%s "
    params.append(asin_choice)

if rating_choice:
    query_conditions += "AND R.rating BETWEEN %s AND %s "
    params.extend(list(rating_choice))

if price_choice:
    query_conditions += "AND B.price BETWEEN %s AND %s "
    params.extend(list(price_choice))

if genre_choice:
    query_conditions += get_disjunction_query("B.genre", genre_choice)
    params.extend(genre_choice)

if keyword_choice:
    query_conditions += "AND S.phrase::tsvector @@ "
    for i in range(len(keyword_choice)):
        if i > 0:
            query_conditions += "|"
        query_conditions += "%s"
    query_conditions += "::tsquery "
    params.extend(keyword_choice)


complete_query = f"SELECT B.title, B.genre, R.rating, R.summary, S.phrase, S.polarity, B.price FROM books as B, reviews as R, sentiments as S WHERE B.asin = R.asin AND R.id = S.review_id {query_conditions}ORDER BY B.asin LIMIT 1000"
filtered = get_data(query=complete_query, search_params=params)
with filtered_results:
    st.write(complete_query, params)
    st.dataframe(filtered.style.format({"price": "${:,.2f}"}))

# TODO full text search
# search for books and return the asin
search_needed = False
search_query_conditions = ""
search_params = []
if title_search:
    search_needed = True
    search_query_conditions += "AND title LIKE %s "
    search_params.append(
        f"%{title_search}%",
    )

if author_search:
    search_needed = True
    search_query_conditions += "AND author LIKE %s "
    search_params = (f"%{author_search}%",)

search_query = f"SELECT asin, title, author FROM books WHERE 1=1 {search_query_conditions}ORDER BY asin"

if search_needed:
    books = get_data(query=search_query, search_params=search_params)
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
