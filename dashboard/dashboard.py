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
    conditions = f"AND {column} IN ("
    for i in range(len(element)):
        if i > 0:
            conditions += ", "
        conditions += "%s"
    conditions += ") "
    return conditions


def get_fts_query(column, words, conjunctive=False):
    """
    returns query and parameter for a full text search with disjunction
    """
    condition = f"AND to_tsvector('simple', {column}) @@ %s::tsquery "
    param = ""
    for i, word in enumerate(words):
        if i > 0:
            param += "&" if conjunctive else "|"
        param += word
    return condition, param


st.title("Book Reviewscope - Amazon Reviews")
# show help text
text, button = st.columns([7, 3])
help_text = (
    "This is a dashboard for accessing the book review scope database which consists of review data written for books on amazon\n\n"
    "In the 'Filter Results' section you can filter the reviews by asin(amazon article ID), User rating, Polarity of a review sentence, Price, Genre and keywords in a review sentence.\n\n"
    "In the 'Book Search' section you can full text search for books by author and/or title e.g. to retrieve the asin.\n\n"
    "For more information visit our [Github](https://github.com/Bort1900/text-tech)"
)
with button:
    help_button = st.button("Show help")
if not "help" in st.session_state.keys():
    st.session_state["help"] = False
if help_button:
    st.session_state["help"] = not st.session_state["help"]

if st.session_state["help"]:
    with text:
        st.markdown(help_text)

# Filter database with various parameters
st.subheader("Filter results")
# Filters
col1, col2 = st.columns([1, 1])
with col1:
    asin_choice = st.text_input(
        "asin",
        help="Amazon standard identification number, can be retrieved via 'Book search'",
    )
with col2:
    genre_choice = st.multiselect("Genres", get_genres())
col3, col4, col5 = st.columns([2, 3, 3])
with col3:
    rating_choice = st.slider("Rating", min_value=1, max_value=5, value=(1, 5))
with col4:
    sentiment_choice = st.segmented_control(
        "Review Polarity",
        options=["negative", "neutral", "positive"],
        selection_mode="multi",
    )
with col5:
    price_choice = st.slider(
        "Price", min_value=0, max_value=100, format="%0.2f", value=(1, 10)
    )
col6, col7 = st.columns([5, 1])
with col6:
    keyword_choice = st_tags(
        label="Keywords:",
        text="Press enter to add more",
    )
with col7:
    toggle_label = st.container()
    toggle_conjunctive = st.toggle("conjuntive", label_visibility="hidden")
    with toggle_label:
        st.markdown("Conjunctive" if toggle_conjunctive else "Disjunctive")

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
    keyword_query, keyword_param = get_fts_query(
        "S.phrase", keyword_choice, conjunctive=toggle_conjunctive
    )
    query_conditions += keyword_query
    params.append(keyword_param)

if sentiment_choice:
    query_conditions += get_disjunction_query("S.polarity", sentiment_choice)
    params += sentiment_choice


complete_query = f"SELECT B.title, B.genre, R.rating, S.phrase, S.polarity, B.price, R.review_text, R.summary FROM books as B, reviews as R, sentiments as S WHERE B.asin = R.asin AND R.id = S.review_id {query_conditions}ORDER BY B.asin LIMIT 1000"
filtered = get_data(query=complete_query, search_params=params)
with filtered_results:
    st.dataframe(filtered.style.format({"price": "${:,.2f}", "rating": "{:,.0f}"}))

# search for books and return the asin
search_needed = False
search_query_conditions = ""
search_params = []
if title_search:
    search_needed = True
    title_query, title_param = get_fts_query(
        "title", title_search.split(), conjunctive=True
    )
    search_query_conditions += title_query
    search_params.append(title_param)

if author_search:
    search_needed = True
    author_query, author_param = get_fts_query(
        "author", author_search.split(), conjunctive=True
    )
    search_query_conditions += author_query
    search_params.append(author_param)

search_query = f"SELECT asin, title, author FROM books WHERE 1=1 {search_query_conditions}ORDER BY asin"

if search_needed:
    books = get_data(query=search_query, search_params=search_params)
    with search_results:
        st.dataframe(books)
