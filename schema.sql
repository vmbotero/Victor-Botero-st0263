CREATE TABLE IF NOT EXISTS peers (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS files (
    filename TEXT,
    peer TEXT,
    FOREIGN KEY (peer) REFERENCES peers(username)
);
