CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rank INTEGER
);

CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    country TEXT,
    year INTEGER
);

CREATE TABLE albums (
    id SERIAL PRIMARY KEY,
    name TEXT,
    artist_id INTEGER REFERENCES artists ON DELETE CASCADE,
    year INTEGER,
    genre TEXT
);

CREATE TABLE tracks (
    id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES artists ON DELETE CASCADE,
    album_id INTEGER REFERENCES albums ON DELETE CASCADE,
    name TEXT,
    length FLOAT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    album_id INTEGER REFERENCES albums ON DELETE CASCADE,
    score INTEGER,
    comment TEXT,
    created TIMESTAMP
);


