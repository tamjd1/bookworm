
"""
Bookmark functionality
"""
import requests

from bookworm import database
from bookworm.utils import get_epoch_millis
from bookworm.query import *
from bookworm import analyzer


# todo :
#        add algorithm to generate recommended article links based on keywords of interest
#        write a proper search algorithm


def search(search_query):
    results = []
    print(search_query)
    with database.con.cursor() as cur:
        cur.execute(SEARCH.format(search_query=search_query))
        for row in cur.fetchall():
            results.append({
                "id": row[0],
                "link": row[1],
                "title": row[2],
                "matchedText": row[3].tobytes()
            })
            cur.execute(VISIT_BOOKMARK.format(bookmark_id=row[0]))
            database.con.commit()
    return results


def add_bookmark(payload):
    print(payload)
    raw_content = requests.get(payload['link']).text
    title = analyzer.get_title(raw_content)
    sanitized_content = analyzer.sanitize(raw_content)
    scores = analyzer.determine_word_scores(sanitized_content)
    word_count = scores["word_count"]
    word_scores = scores["word_scores"]
    word_frequency = {x["word"]: x["count"] for x in word_scores}
    highlights = analyzer.generate_highlights(sanitized_content, word_frequency)
    with database.con.cursor() as cur:
        cur.execute(ADD_BOOKMARK.format(
            title=title, link=payload['link'], created_at=get_epoch_millis(), updated_at=get_epoch_millis(),
            highlights=highlights, raw_data=raw_content, sanitized_data=sanitized_content, word_count=word_count
        ))
        bookmark_id = cur.fetchone()[0]
        database.con.commit()

        values = [(bookmark_id, x["word"], x["stem"], x["count"], x["tf"], x["idf"]) for x in word_scores]
        cur.execute("""
            insert into bookworm.keywords (bookmark_id, word, stem, count, tf, idf)
            values {}
        """.format(values))

        # TODO: Update recommendation table (in subprocess)

    return {"id": bookmark_id, "link": payload['link']}


def delete_bookmark(bookmark_id):
    print(bookmark_id)
    with database.con.cursor() as cur:
        cur.execute(DELETE_BOOKMARK.format(id=bookmark_id))
        database.con.commit()
    return {"DELETED": "{bookmark_id}".format(bookmark_id=bookmark_id)}


def get_metadata():
    with database.con.cursor() as cur:
        cur.execute(META_DATA_TOTAL)
        total = cur.fetchone()[0]
        cur.execute(META_DATA_MOST_VISITED)
        most_visited = cur.fetchone()[0]
        cur.execute(META_DATA_LATEST)
        latest = cur.fetchone()[0]
        cur.execute(META_DATA_OLDEST)
        oldest = cur.fetchone()[0]

    return {
        "totalBookmarks": total,
        "mostVisited": most_visited,
        "latest": latest,
        "oldest": oldest
    }


def get_recommended():
    result = []
    with database.con.cursor() as cur:
        cur.execute(GET_RECOMMENDED)
        for row in cur.fetchall():
            result.append({
                "title": row[0],
                "highlights": row[1]
            })
    return result


def get_summary_highlights(bookmark_id):
    print(bookmark_id)
    with database.con.cursor() as cur:
        cur.execute(GET_SUMMARY_HIGHLIGHTS.format(bookmark_id=bookmark_id))
        data = cur.fetchone()

    return {
        "title": data[0],
        "highlights": data[1]
    }
