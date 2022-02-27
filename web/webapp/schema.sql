DROP TABLE IF EXISTS passkeys;

CREATE TABLE passkeys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  passkey TEXT UNIQUE NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  used INTEGER,
  admin INTEGER NOT NULL DEFAULT 0,
  expiration TIMESTAMP,
  num_uses INTEGER,
  notes TEXT
);