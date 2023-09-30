CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(256) UNIQUE,
    encoded_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rated_movies INTEGER NOT NULL,
    rated_series INTEGER NOT NULL,
    reviews INTEGER NOT NULL,
    followers INTEGER NOT NULL,
    following INTEGER NOT NULL,
    favourites INTEGER NOT NULL
);
