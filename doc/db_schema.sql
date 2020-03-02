DROP TABLE IF EXISTS bookworm.bookmarks CASCADE;
CREATE TABLE bookworm.bookmarks (
	id serial PRIMARY KEY,
	title text NOT NULL,
	link text NOT NULL,
	created_at bigint NOT NULL,
	updated_at bigint NOT NULL,
	highlights jsonb NULL,
	raw_data bytea NULL,
	sanitized_data bytea NULL
);

DROP TABLE IF EXISTS bookworm.meta_data CASCADE;
CREATE TABLE bookworm.meta_data (
	id serial PRIMARY KEY,
	visited_count int NULL,
	last_visited_at bigint NULL,
	bookmark_id int REFERENCES bookworm.bookmarks(id)
);

DROP TABLE IF EXISTS bookworm.keyword_scores CASCADE;
CREATE TABLE bookworm.keyword_scores (
	id serial PRIMARY KEY,
	keywords text NOT NULL,
	tf_ids_scores numeric NULL,
	bookmark_id int REFERENCES bookworm.bookmarks(id)
);

DROP TABLE IF EXISTS bookworm.recommendations;
CREATE TABLE bookworm.recommendations (
	id serial PRIMARY KEY,
	title text NOT NULL,
	date_recommended bigint NULL,
	date_analyzed bigint NULL,
	highlights jsonb NULL,
	based_on_keyworkds jsonb NULL
);