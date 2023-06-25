BEGIN;

CREATE TABLE users (
    id UUID NOT NULL,
    username VARCHAR(64) UNIQUE NOT NULL,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE movies (
    id UUID NOT NULL,
    title VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL,
    rating REAL NOT NULL,
    rating_count INTEGER NOT NULL
);

COMMIT;