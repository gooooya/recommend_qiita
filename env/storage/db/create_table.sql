CREATE TABLE learning_resources (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(8000) NOT NULL UNIQUE,
    created_date TIMESTAMP  NOT NULL,
    learned BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_created_date ON learning_resources(created_date);

