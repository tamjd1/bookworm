

def api_help():
    return [
        {
            "API": "/init",
            "description": "to initialize bookworm database by bulk loading an array of bookmark links",
            "method": "POST",
            "payload": {
                "bookmarks": [
                    {"chromeId": 1, "link": "link to bookmark"},
                    {"chromeId": 2, "link": "link to bookmark"},
                    {"chromeId": 3, "link": "link to bookmark"},
                    {"chromeId": 5, "link": "link to bookmark"}
                ]
            },
            "responseCode": 201,
            "response": {
                "message": "bookworm initialization has begun with the provided bookmarks",
                "statusCode": 201
            }
        },
        {
            "API": "/search?q=search keywords",
            "description": "to search for keywords",
            "method": "GET",
            "responseCode": 200,
            "response":
                [
                    {"chromeId": 1, "title": "ABC", "matchedText": "keyword1"},
                    {"chromeId": 2, "title": "DEF", "matchedText": "keyword2"}
                ]
         },
        {
            "API": "/bookmark",
            "description": "to add bookmark specifically from bookworm",
            "method": "POST",
            "payload": {
                "chromeId": 2,
                "link": "link to bookmark"
            },
            "responseCode": 200,
            "response": {
                "id": 1,
                "chromeId": 2,
                "link": "link to bookmark"
            }
        },
        {
            "API": "/bookmark/<int:chrome_id>",
            "description": "to delete bookmark specifically from bookworm",
            "method": "DELETE",
            "responseCode": 200,
            "response": {"DELETED": 3}
        },
        {
            "API": "/metadata",
            "description": "to get bookworm metadata",
            "method": "GET",
            "responseCode": 200,
            "response":
                {
                    "totalBookmarks": 12,
                    "mostVisited": "title7",
                    "mostVisitedChromeId": 1,
                    "latest": "title12",
                    "latestChromeId": 2,
                    "oldest": "title1",
                    "oldestChromeId": 3
                }
        },
        {
            "API": "/recommended",
            "description": "to get recommended link based on popular keywords",
            "method": "GET",
            "responseCode": 200,
            "response":
                {
                    "title": "TITLE6",
                    "highlights": ["abc", "def", "ghi"],
                    "chromeId": 2
                }
        },
        {
            "API": "/highlights/<int:chrome_id>",
            "description": "to get get summary highlights",
            "method": "GET",
            "responseCode": 200,
            "response":
                {
                    "title": "TITLE5",
                    "highlights": ["abc", "def", "ghi"],
                    "chromeId": 3
                }
        }
    ]
