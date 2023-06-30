BEGIN;

CREATE TABLE users (
    id UUID UNIQUE NOT NULL,
    username VARCHAR(64) UNIQUE NOT NULL,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE movies (
    id UUID UNIQUE NOT NULL,
    title VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL,
    rating REAL NOT NULL,
    rating_count INTEGER NOT NULL
);

CREATE TABLE user_movie_ratings (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
    rating REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

COMMIT;