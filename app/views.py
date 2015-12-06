from app import app, cache
from flask import request, render_template, Response

import hashlib
import random

@app.route('/')
def index():
    return render_template('main.html',
            title = "Utils")

@app.route('/ip')
def ip():
    addr = request.remote_addr
    if addr.startswith('::ffff:'):
        addr = addr.split(':')[-1]
    return Response(addr, mimetype="text/plain")

@app.route('/user_agent')
def user_agent():
    return Response(request.user_agent.string, mimetype="text/plain")

@app.route('/request_body', methods=['GET', 'POST'])
def request_body():
    return Response(request.environ['body_copy'], mimetype="text/plain")

@app.route('/request_headers', methods=['GET', 'POST'])
def request_headers():
    return Response(str(request.headers), mimetype="text/plain")

@app.route('/md5sum', methods=['GET', 'POST'])
def md5sum():
    text = request.values.get('text', '')
    return Response(hashlib.md5(text.encode()).hexdigest(), mimetype="text/plain")

@app.route('/sha1sum', methods=['GET', 'POST'])
def sha1sum():
    ver = request.values.get('ver', '1')
    text = request.values.get('text', '')

    hashes = {
        '1': hashlib.sha1,
        '224': hashlib.sha224,
        '256': hashlib.sha256,
        '384': hashlib.sha384,
        '512': hashlib.sha512
    }

    try:
        hash_obj = hashes[ver]
    except KeyError:
        return Response(status=400)

    return Response(hash_obj(text.encode()).hexdigest(), mimetype="text/plain")

@app.route('/fortune')
def fortune():
    options = {
        'all': ('fortune_count', 'fortune_%d'),
        'off': ('offensive_fortune_count', 'offensive_fortune_%d'),
        'tame': ('tame_fortune_count', 'tame_fortune_%d')
    }

    intersection = set(request.values.keys()) & set(options.keys())
    if intersection:
        selection = intersection.pop()
    else:
        selection = 'tame'

    count, key = options[selection]

    fortune_number = random.randrange(0, cache.get(count))
    fortune = cache.get(key % fortune_number)

    return Response(fortune[1].strip(), mimetype="text/plain")
