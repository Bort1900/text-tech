Project Group Book Review Scope for Text Technology Course Summer 2025

Our project works with Amazon book review data applying polarity and making properties accessible via a dashboard.
The dashboard is hosted on https://book-review-scope.streamlit.app/ and allows filtering for review and metadata properties.
This way conclusions over certain review aspects and their correlations to the rating can be drawn.
The code for the streamlit app can be found in the dashboard folder.

The notebooks folder contains several notebooks with scripts that were used to prepare the data:
1. filter_by_genre.ipynb takes the amazon book metadata and review data (https://amazon-reviews-2023.github.io/) and extracts a random sample.
2. merge_data.ipynb merges the two json data files to one json file with the relevant data for all the reviews.
3. clean_data.ipynb applies some preparation to string data especially reviews and splits them into sentences.
4. extract_phrases.ipynb assigns a sentiment score to the particular review sentences and assigns a polarity.
5. xml_exporter.ipynb writes the processed data into an xml file and validates it according to the schema in the schema folder.
6. db_insert.ipynb creates an SQLite database from the sql file in the schema folder and fills the tables with the review data.
7. analysis.ipynb was an original notebook to work with the database
8. migrate_database.ipynb translates the database to PostgreSQL and moves it to a database server

The schema folder contains the XML Relax NG Grammar as well as the SQL file defining the database tables.
