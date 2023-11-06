CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE movies (
    id UUID PRIMARY KEY,
    en_name VARCHAR NOT NULL,
    user_rating_count INTEGER NOT NULL,
    user_rating NUMERIC(2, 4),
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE movie_ratings (
    user_id UUID FOREIGN KEY REFERENCES users(id),
    movie_id UUID FOREIGN KEY REFERENCES movies(id),
    rating NUMERIC(2, 1) NOT NULL,
    is_full BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ
);

CREATE TABLE movie_ratings_policy (
    required_rated_movies_count SMALLINT,
    required_time_pass_after_registration SMALLINT
);