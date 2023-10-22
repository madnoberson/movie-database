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

CREATE TABLE adding_tasks (
    id UUID PRIMARY KEY,
    creator_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    adding_type SMALLINT NOT NULL,
    kinopoisk_id VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    related_to UUID UNIQUE,
    finished_at TIMESTAMPTZ
);