BEGIN;

CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE genres (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL
);

INSERT INTO genres
    (id, name)
VALUES 
    (0, 'Action'),
    (1, 'Thriller'),
    (2, 'Comedy'),
    (3, 'War'),
    (4, 'Documentary'),
    (5, 'Crime'),
    (6, 'Drama'),
    (7, 'Romance'),
    (8, 'Fantasy'),
    (9, 'Adventure'),
    (10, 'Horror'),
    (11, 'Musical'),
    (12, 'Mystery'),
    (13, 'Science fiction'),
    (14, 'Western'),
    (15, 'History'),
    (16, 'Biography'),
    (17, 'Animation')
;

CREATE TABLE movies (
    id UUID PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL,
    rating REAL NOT NULL,
    rating_count INTEGER NOT NULL,
    status SMALLINT,
    mpaa SMALLINT,
    poster_key VARCHAR(128) UNIQUE
);

CREATE TABLE movies_genres (
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
    genre_id SMALLINT REFERENCES genres(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE user_movie_ratings (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    movie_id UUID REFERENCES movies(id) ON DELETE CASCADE NOT NULL,
    rating REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

COMMIT;