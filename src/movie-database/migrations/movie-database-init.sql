CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE movies (
    id UUID PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE enrichment_tasks (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    enrichment_type SMALLINT NOT NULL,
    kinopoisk_id VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    movie_id UUID REFERENCES movies(id),
    finished_at TIMESTAMPTZ
);