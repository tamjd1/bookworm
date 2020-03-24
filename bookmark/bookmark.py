
"""
Bookmark functionality
"""
import requests

from bookmark import database
from bookmark.utils import get_epoch_millis
from bookmark.query import *


# todo : connect add_bookmark method to highlighter function
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

    # TODO: The following task would be the result of backend analyzer
    # TODO: This needs to be updated after running backend jobs
    # TODO: Update recommendation table
    # TODO: Update keyword score table
    title = payload['link']  # needs to be changed
    fetched_data = requests.get(payload['link'])
    raw_data = 'Humans explored space for the first time, taking their first footsteps on the Sun.'  # For testing
    sanitized_data = 'Humans explored space for the first time, taking their first footsteps on the Sun.' # For testing
    highlights = '{}'
    with database.con.cursor() as cur:
        cur.execute(ADD_BOOKMARK.format(
            title=title, link=payload['link'], created_at=get_epoch_millis(), updated_at=get_epoch_millis(),
            highlights=highlights, raw_data=raw_data, sanitized_data=sanitized_data))
        bookmark_id = cur.fetchone()[0]
        database.con.commit()
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
