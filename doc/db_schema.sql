DROP TABLE IF EXISTS bookworm.bookmarks CASCADE;
CREATE TABLE bookworm.bookmarks (
	id serial PRIMARY KEY,
	title text NOT NULL,
	link text NOT NULL,
	created_at bigint NOT NULL,
	updated_at bigint NOT NULL,
	visited_count int DEFAULT 1,
	highlights jsonb NULL,
	raw_data bytes NULL,
	sanitized_data bytes NULL
);


DROP TABLE IF EXISTS bookworm.keyword_scores CASCADE;
CREATE TABLE bookworm.keyword_scores (
	id serial PRIMARY KEY,
	stem text NOT NULL,
	word text NOT NULL,
	count int NOT NULL,
	tf float not null,
	idf float not null,
	bookmark_id int REFERENCES bookworm.bookmarks(id)
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS bookworm.recommendations;
CREATE TABLE bookworm.recommendations (
	id serial PRIMARY KEY,
	title text NOT NULL,
	date_recommended bigint NULL,
	date_analyzed bigint NULL,
	highlights jsonb NULL,
	based_on_keywords jsonb NULL,
	bookmark_id int REFERENCES bookworm.bookmarks(id)
	ON DELETE CASCADE
);