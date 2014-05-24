from app import app
from flask import request, url_for, render_template, Response

import hashlib
import subprocess

@app.route('/')
def index():
    return render_template('main.html',
            title = "Utils")

@app.route('/my_ip')
def my_ip():
    return Response(request.remote_addr, mimetype="text/plain")

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
    return Response(hashlib.md5(text).hexdigest(), mimetype="text/plain")

@app.route('/sha1sum', methods=['GET', 'POST'])
def sha1sum():
    ver = request.values.get('ver', '1')
    text = request.values.get('text', '')

    hash_obj = None

    if ver == '1':
        hash_obj = hashlib.sha1(text)
    elif ver == '224':
        hash_obj = hashlib.sha224(text)
    elif ver == '256':
        hash_obj = hashlib.sha256(text)
    elif ver == '384':
        hash_obj = hashlib.sha384(text)
    elif ver == '512':
        hash_obj = hashlib.sha512(text)
    else:
        return ''

    return Response(hash_obj.hexdigest(), mimetype="text/plain")

@app.route('/fortune')
def fortune():
    opt_trans = {'all': '-a', 'offensive': '-o'}

    opt = request.values.get('opt', '')
    param = opt_trans.get(opt, '')

    ret = ''

    try:
        ret = str(subprocess.check_output(["/usr/games/fortune", param]))
    except:
        pass

    return Response(ret, mimetype="text/plain")
