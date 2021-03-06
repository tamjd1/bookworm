#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA $POSTGRES_SCHEMA;
    CREATE TABLE $POSTGRES_SCHEMA.bookmarks (
      id serial PRIMARY KEY,
      chrome_id int NOT NULL UNIQUE,
      title text NOT NULL,
      link text NOT NULL,
      created_at bigint NOT NULL,
      updated_at bigint NOT NULL,
      visited_count int DEFAULT 1,
      highlights jsonb NULL,
      raw_data bytea NULL,
      sanitized_data bytea NULL
    );
    CREATE TABLE $POSTGRES_SCHEMA.keywords (
      id serial PRIMARY KEY,
      stem text NOT NULL,
      word text NOT NULL,
      count int NOT NULL,
      tf_idf_score float NOT NULL,
      bookmark_id int REFERENCES $POSTGRES_SCHEMA.bookmarks(id)
      ON DELETE CASCADE
    );
    CREATE TABLE $POSTGRES_SCHEMA.recommendations (
      id serial PRIMARY KEY,
      title text NOT NULL,
      date_recommended bigint NULL,
      date_analyzed bigint NULL,
      highlights jsonb NULL,
      based_on_keywords jsonb NULL,
      bookmark_id int REFERENCES $POSTGRES_SCHEMA.bookmarks(id)
      ON DELETE CASCADE
    );
EOSQL