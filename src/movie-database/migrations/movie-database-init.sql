CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);