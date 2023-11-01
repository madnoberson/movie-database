CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE movies (
    id UUID PRIMARY KEY,
    en_name VARCHAR NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);