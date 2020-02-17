import requests
from flask import Flask
from elasticsearch import Elasticsearch
from rapidjson import dumps

from scripts.utils import get_headers

app = Flask(__name__)
es = Elasticsearch(['http://elastic:9200/'], verify_certs=True)


@app.route('/')
def hello():
    response = {"message": "Hello, World"}
    return dumps(response), 200, get_headers(response)


@app.route('/elastic')
def elastic():
    return es.info()
