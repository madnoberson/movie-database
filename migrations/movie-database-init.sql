CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    username VARCHAR(64) UNIQUE NOT NULL
);