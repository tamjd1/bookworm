
"""
Work In Progress
"""


def search(query):
    print(query)
    return [
        {"title": "TITLE1", "matchedText": "title1"},
        {"title": "TITLE2", "matchedText": "title2"}
    ]


def add_bookmark(payload):
    print(payload)
    return {"id": 1, "link": payload['link']}


def delete_bookmark(bookmark_id):
    print(bookmark_id)
    return {"DELETED": "{bookmark_id}".format(bookmark_id=bookmark_id)}


def get_metadata():
    return {"totalBookmarks": 12, "mostVisited": "title7", "latest": "title12", "oldest": "title1"}


def get_recommended():
    return {"title": "TITLE6", "highlights": ["abc", "def", "ghi"]}


def get_summary_highlights(bookmark_id):
    print(bookmark_id)
    return {"title": "TITLE5", "highlights": ["abc", "def", "ghi"]}