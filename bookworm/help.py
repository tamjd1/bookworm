

def api_help():
    return [
        {
            "API": "/search?q=search keywords",
            "description": "to search for keywords",
            "method": "GET",
            "responseCode": 200,
            "response":
                [
                    {"title": "ABC", "matchedText": "keyword1"},
                    {"title": "DEF", "matchedText": "keyword2"}
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
                    "latest": "title12",
                    "oldest": "title1"
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
                    "highlights": ["abc", "def", "ghi"]
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
                    "highlights": ["abc", "def", "ghi"]
                }
        }
    ]
