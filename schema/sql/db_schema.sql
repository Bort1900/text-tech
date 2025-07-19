-- table for books and their metadata
CREATE TABLE IF NOT EXISTS books (
    asin TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    price REAL,
    genre TEXT
);
-- enumerated table for review data corresponding to books
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asin TEXT,
    rating REAL,
    review_text TEXT,
    summary TEXT,
    FOREIGN KEY(asin) REFERENCES books(asin)
);
-- enumerated table for phrases and their polarities corresponding to a book review
CREATE TABLE IF NOT EXISTS sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER,
    phrase TEXT,
    polarity TEXT,
    FOREIGN KEY(review_id) REFERENCES reviews(id)
);
