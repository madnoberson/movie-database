BEGIN;

CREATE TABLE users (
    id UUID NOT NULL,
    username VARCHAR(64) UNIQUE NOT NULL,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

COMMIT;