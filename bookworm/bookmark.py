
"""
Bookmark functionality
"""
import requests

from bookworm import database
from bookworm.utils import get_epoch_millis
from bookworm import analyzer


# todo :
#        add algorithm to generate recommended article links based on keywords of interest


def search(search_query):
    results = []
    print(search_query)
    stemmed_search_terms = analyzer.word_stemmer(search_query)
    with database.con.cursor() as cur:
        query = cur.mogrify("""select distinct a.id, a.chrome_id, a.link, a.title, a.sanitized_data, c.tf_idf_score
                        from bookmarks a
                        join keywords b on a.id = b.bookmark_id
                        join keyword_scores c on b.stem = c.stem
                        where c.stem in %s
                          and c.tf_idf_score > 0
                        order by c.tf_idf_score
                        limit 10
        """, (tuple(stemmed_search_terms),))
        cur.execute(query)
        for row in cur.fetchall():
            print(row)
            results.append({
                "id": row[0],
                "chromeId": row[1],
                "link": row[2],
                "title": row[3],
                "score": row[5],
                "matchedText": "...".join(analyzer.get_matching_sentences(row[4].tobytes().decode('utf-8'), search_query))
            })
            cur.execute("UPDATE bookmarks SET visited_count = visited_count + 1 WHERE id = {bookmark_id}".format(
                bookmark_id=row[0]))
            database.con.commit()
    return results


def add_bookmark(payload):
    print(payload)
    with database.con.cursor() as cur:
        cur.execute("select id from bookmarks where chrome_id = {} limit 1".format(payload["chromeId"]))
        row_count = cur.rowcount
        if row_count == 1:
            bookmark_id = cur.fetchone()[0]
            return {
                "id": bookmark_id,
                "link": payload['link'],
                "chromeId": payload['chromeId']
            }  # bookmark exists; no need for analysis

    raw_content = requests.get(payload['link']).text
    title = analyzer.get_title(raw_content)
    sanitized_content = analyzer.sanitize(raw_content)
    scores = analyzer.determine_word_scores(sanitized_content)
    word_count = scores["word_count"]
    word_scores = scores["word_scores"]
    word_frequency = {x["word"]: x["count"] for x in word_scores}
    highlights = analyzer.generate_highlights(sanitized_content, word_frequency)
    with database.con.cursor() as cur:
        query = cur.mogrify("""INSERT INTO bookmarks (chrome_id, title, link, created_at, updated_at, highlights, sanitized_data)
                               VALUES (%(chrome_id)s, %(title)s, %(link)s, %(created_at)s, %(updated_at)s, %(highlights)s, %(sanitized_data)s)
                               RETURNING id
        """, {
            "chrome_id": payload['chromeId'], "title": title, "link": payload['link'], "created_at": get_epoch_millis(),
            "updated_at": get_epoch_millis(), "highlights": highlights, "sanitized_data": sanitized_content
        })
        cur.execute(query)
        bookmark_id = cur.fetchone()[0]

        values = [(bookmark_id, x["word"], x["stem"], x["count"]) for x in word_scores]
        args_str = b','.join(cur.mogrify("(%s,%s,%s,%s)", x) for x in values)
        query = cur.mogrify(b"insert into bookworm.keywords (bookmark_id, word, stem, count) values " + args_str)
        cur.execute(query)

        values = [(x["stem"], x["tf_idf_score"]) for x in word_scores]
        args_str = b','.join(cur.mogrify("(%s,%s)", x) for x in values)
        query = cur.mogrify(b"insert into bookworm.keyword_scores (stem, tf_idf_score) values " + args_str +
                            b" on conflict (stem) do update set tf_idf_score = excluded.tf_idf_score ")
        cur.execute(query)

        database.con.commit()

        # TODO: Update recommendation table (in subprocess)

    return {
        "id": bookmark_id,
        "link": payload['link'],
        "chromeId": payload['chromeId']
    }


def delete_bookmark(chrome_id):
    print(chrome_id)
    with database.con.cursor() as cur:
        cur.execute("DELETE FROM bookmarks WHERE chrome_id = {chrome_id};".format(chrome_id=chrome_id))
        database.con.commit()
    return {"DELETED": "{chrome_id}".format(chrome_id=chrome_id)}


def get_metadata():
    most_visited = [None, None]
    latest = [None, None]
    oldest = [None, None]
    with database.con.cursor() as cur:
        cur.execute("SELECT count(id) FROM bookmarks;")
        total = cur.fetchone()[0]
        if total > 0:
            cur.execute("""SELECT chrome_id, title FROM bookmarks WHERE
             visited_count = (SELECT max(visited_count) FROM bookmarks);""")
            most_visited = cur.fetchone()
            cur.execute("""SELECT chrome_id, title FROM bookmarks WHERE
             created_at = (SELECT max(created_at) FROM bookmarks);""")
            latest = cur.fetchone()
            cur.execute("""SELECT chrome_id, title FROM bookmarks WHERE
             created_at = (SELECT min(created_at) FROM bookmarks);""")
            oldest = cur.fetchone()

    return {
        "totalBookmarks": total,
        "mostVisited": most_visited[1],
        "mostVisitedChromeId": most_visited[0],
        "latest": latest[1],
        "latestChromeId": latest[0],
        "oldest": oldest[1],
        "oldestChromeId": oldest[0]
    }


def get_recommended():
    result = []
    with database.con.cursor() as cur:
        cur.execute("SELECT chrome_id, title, highlights FROM recommendations;")
        for row in cur.fetchall():
            result.append({
                "chromeId": row[0],
                "title": row[1],
                "highlights": row[2]
            })
    return result


def get_summary_highlights(chrome_id):
    print(chrome_id)
    title = None
    highlights = None
    with database.con.cursor() as cur:
        cur.execute("SELECT title, highlights FROM bookmarks WHERE chrome_id = {chrome_id};".format(
            chrome_id=chrome_id))
        data = cur.fetchone()
        if data:
            title = data[0]
            highlights = data[1]

    return {
        "chromeId": chrome_id,
        "title": title,
        "highlights": highlights
    }
