from app import app, cache
from flask import request, render_template, Response

import random


@app.route('/')
def index():
    return render_template('main.html', title="Utils")


@app.route('/raw/ip')
def ip():
    addr = request.remote_addr
    if addr.startswith('::ffff:'):
        addr = addr.split(':')[-1]
    return Response(addr, mimetype="text/plain")


@app.route('/raw/user-agent')
def user_agent():
    return Response(request.user_agent.string, mimetype="text/plain")


@app.route('/raw/request-body', methods=['GET', 'POST'])
def request_body():
    return Response(request.environ['body_copy'], mimetype="text/plain")


@app.route('/raw/request-headers', methods=['GET', 'POST'])
def request_headers():
    return Response(str(request.headers), mimetype="text/plain")


@app.route('/raw/fortune')
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

    return Response(fortune.strip(), mimetype="text/plain")


@app.route('/amionline')
@app.route('/amionline/<string:foo>', methods=['GET', 'POST'])
def amionline(foo=None):
    if foo is None:
        res = "Usage: GET /amionline/RANDOM_STRING"
    else:
        res = foo

    return Response(res, mimetype="text/plain")


@app.route('/random-name')
def random_name():
    return render_template('random-name.html')


@app.route('/timer')
def timer():
    return render_template('timer.html')


@app.route('/robots.txt')
def robots_txt():
    return render_template('robots.txt')
