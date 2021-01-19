CREATE TABLE IF NOT EXISTS links(
	id integer PRIMARY KEY AUTOINCREMENT,
	full_link text NOT NULL,
	short_link text NOT NULL
);