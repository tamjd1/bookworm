
ADD_BOOKMARK = "INSERT INTO bookmarks (title, link, created_at, updated_at, highlights, raw_data, sanitized_data) " \
               "VALUES ('{title}', '{link}', {created_at}, {updated_at}, '{highlights}', '{raw_data}', " \
               "'{sanitized_data}') RETURNING id;"

DELETE_BOOKMARK = "DELETE FROM bookmarks WHERE id = {id};"

META_DATA_TOTAL = "SELECT count(id) FROM bookmarks;"
META_DATA_LATEST = "SELECT title FROM bookmarks WHERE created_at = (SELECT max(created_at) FROM bookmarks);"
META_DATA_OLDEST = "SELECT title FROM bookmarks WHERE created_at = (SELECT min(created_at) FROM bookmarks);"
META_DATA_MOST_VISITED = "SELECT title FROM bookmarks WHERE visited_count = (SELECT max(visited_count) FROM bookmarks);"

GET_RECOMMENDED = "SELECT title, highlights FROM recommendations;"

GET_SUMMARY_HIGHLIGHTS = "SELECT title, highlights FROM bookmarks WHERE id = {bookmark_id};"


SEARCH = "SELECT id, link, title, sanitized_data FROM bookmarks WHERE sanitized_data like '%{search_query}%';"
VISIT_BOOKMARK = "UPDATE bookmarks SET visited_count = visited_count + 1 WHERE id = {bookmark_id}"
