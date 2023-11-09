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
    user_rating REAL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE movie_ratings (
    user_id UUID,
    movie_id UUID,
    rating REAL NOT NULL,
    is_full BOOLEAN NOT NULL,   
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE movies_rating_policy (
    required_rated_movie_count SMALLINT,
    required_days_pass_after_registration SMALLINT
);

INSERT INTO movies_rating_policy VALUES (10, 1);

CREATE TABLE filmophile_achievements (
    id SMALLINT PRIMARY KEY,
    title VARCHAR NOT NULL,
    required_rated_movie_count SMALLINT
);

INSERT INTO filmophile_achievements VALUES 
(0, 'Beginner filmophile', 1), (1, 'Advanced beginner filmophile', 100),
(2, 'Advanced filmophile', 500), (3, 'Veteran filmophile', 1000);

CREATE TABLE user_achievements (
    user_id UUID NOT NULL,
    type SMALLINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (user_id, type),
    FOREIGN KEY (user_id) REFERENCES users(id)
);