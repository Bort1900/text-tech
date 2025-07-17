CREATE TABLE IF NOT EXISTS books (
    asin TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    price REAL,
    genre TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asin TEXT,
    rating REAL,
    review_text TEXT,
    summary TEXT,
    FOREIGN KEY(asin) REFERENCES books(asin)
);

CREATE TABLE IF NOT EXISTS sentiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_id INTEGER,
    phrase TEXT,
    polarity TEXT,
    FOREIGN KEY(review_id) REFERENCES reviews(id)
);
