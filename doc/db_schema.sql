DROP TABLE IF EXISTS bookworm.bookmarks CASCADE;
CREATE TABLE bookworm.bookmarks (
	id serial PRIMARY KEY,
	title text NOT NULL,
	link text NOT NULL,
	created_at bigint NOT NULL,
	updated_at bigint NOT NULL,
	visited_count int DEFAULT 1,
	highlights jsonb NULL,
	raw_data bytea NULL,
	sanitized_data bytea NULL
);


DROP TABLE IF EXISTS bookworm.keyword_scores CASCADE;
CREATE TABLE bookworm.keyword_scores (
	id serial PRIMARY KEY,
	keywords text NOT NULL,
	tf_ids_scores numeric NULL,
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