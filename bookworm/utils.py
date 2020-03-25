
from flask import request
import time


def get_headers(response):
    try:
        origin = request.headers['Origin']
        cred = 'true'
    except:
        origin = '*'
        cred = 'false'
    return [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', origin),
        ('Access-Control-Allow-Credentials', cred),
        ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization'),
        ('Connection', 'close'),
        ('content-length', str(len(response)))
    ]


def get_epoch_millis():
    """Get the current epoch time in milliseconds"""
    return int(time.time() * 1000)
