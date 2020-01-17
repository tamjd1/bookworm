import requests
from flask import Flask
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(['http://elastic:9200/'], verify_certs=True)


@app.route('/')
def hello():
    return "Hello, World"


@app.route('/elastic')
def elastic():
    return es.info()
