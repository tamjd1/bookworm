from flask import Flask, request
from rapidjson import dumps, loads
import threading

from bookworm.utils import get_headers
from bookworm.help import api_help
from bookworm import bookmark
from bookworm import database, config

app = Flask(__name__)


@app.route('/health')
def health():
    print('I am healthy :)')
    response = {"health": "OK"}
    return dumps(response), 200, get_headers(response)


@app.route('/help')
def help_api():
    print('Helping ...')
    response = api_help()
    return dumps(response), 200, get_headers(response)


@app.route('/search')
def search():
    print('Searching...')
    search_query = request.args.get('q')
    response = bookmark.search(search_query)
    return dumps(response), 200, get_headers(response)


@app.route('/bookmark', methods=['POST'])
def add_bookmark():
    print('Adding Bookmark...')
    payload = request.get_json()
    response = bookmark.add_bookmark(payload)
    return dumps(response), 200, get_headers(response)


def __initialize_bookworm(bookmarks):
    for b in bookmarks:
        bookmark.add_bookmark(b)


@app.route('/init', methods=['POST'])
def _init():
    print("Initializing bookworm...")
    payload = request.get_json()
    bookmarks = payload["bookmarks"]
    t = threading.Thread(target=__initialize_bookworm, args=(bookmarks,))
    t.start()
    response = {"message": "bookworm initialization has begun with the provided bookmarks", "statusCode": 201}
    return dumps(response), 201, get_headers(response)


@app.route('/bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    print('Deleting Bookmark...')
    response = bookmark.delete_bookmark(bookmark_id)
    return dumps(response), 200, get_headers(response)


@app.route('/metadata')
def get_metadata():
    print('Getting metadata...')
    response = bookmark.get_metadata()
    return dumps(response), 200, get_headers(response)


@app.route('/recommended')
def get_recommended():
    print('Getting recommended...')
    response = bookmark.get_recommended()
    return dumps(response), 200, get_headers(response)


@app.route('/highlights/<int:bookmark_id>')
def get_summary_highlights(bookmark_id):
    print('Getting summary highlights for {bookmark_id}...'.format(bookmark_id=bookmark_id))
    response = bookmark.get_summary_highlights(bookmark_id)
    return dumps(response), 200, get_headers(response)


@app.before_first_request
def initialize_db_connection():
    database.initialize_connection(config.database)
