CREATE TABLE superusers (
    id UUID PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL,
    permissions JSON NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);