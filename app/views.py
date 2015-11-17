from app import app
from flask import request, render_template, Response

import hashlib
import subprocess

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
    opt_trans = {'all': '-a', 'offensive': '-o'}

    opt = request.values.get('opt', '')
    param = opt_trans.get(opt, '')

    ret = ''

    try:
        ret = subprocess.check_output(["/usr/games/fortune", param]).decode()
    except:
        pass

    return Response(ret, mimetype="text/plain")
