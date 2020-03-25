#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE SCHEMA $POSTGRES_SCHEMA;
    CREATE TABLE $POSTGRES_SCHEMA.bookmarks (
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
    CREATE TABLE $POSTGRES_SCHEMA.keyword_scores (
      id serial PRIMARY KEY,
      stem text NOT NULL,
      word text NOT NULL,
      count int NOT NULL,
      tf float not null,
      idf float not null,
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