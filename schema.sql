CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    rank INTEGER
);

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name TEXT,
    country TEXT,
    year INTEGER,
    genre TEXT
);

CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    artist_id INTEGER REFERENCES artists,
    year INTEGER
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    album_id INTEGER REFERENCES albums,
    score INTEGER,
    comment TEXT
);
