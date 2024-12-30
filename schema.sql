CREATE TABLE user (
  sn INTEGER PRIMARY KEY AUTOINCREMENT,
  id TEXT,
  name TEXT NOT NULL,
  email TEXT,
  profile_pic TEXT,
  password_hash TEXT
);
CREATE TABLE watchlist (
  sn INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  movie_id INTEGER
);