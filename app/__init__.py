from flask import Flask
from flask.ext.cache import Cache

import pathlib
import codecs


class WSGICopyBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        from io import BytesIO
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['body_copy'] = body
        environ['wsgi.input'] = BytesIO(body)

        # Call the wrapped application
        app_iter = self.application(environ,
                                    self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):

            # Call upstream start_response
            start_response(status, headers, exc_info)
        return callback

app = Flask(__name__)
app.wsgi_app = WSGICopyBody(app.wsgi_app)


class IncCache(Cache):
    def inc(self, *args, **kwargs):
        return self.cache.inc(*args, **kwargs)

cache = IncCache(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 2**32})

# cache fortunes
fortunes_path = pathlib.Path('/usr/share/games/fortunes')
tame_fortunes_paths = fortunes_path.glob('*.u8')
offensive_fortunes_paths = fortunes_path.glob('off/*.u8')

offensive_fortunes = []
for p in offensive_fortunes_paths:
    with p.open() as f:
        offensive_fortunes.extend(codecs.decode(f.read(), 'rot13').split('%'))

tame_fortunes = []
for p in tame_fortunes_paths:
    with p.open() as f:
        tame_fortunes.extend(f.read().split('%'))

for fortune in enumerate(offensive_fortunes):
    off_count = cache.inc('offensive_fortune_count')
    all_count = cache.inc('fortune_count')
    cache.set('offensive_fortune_%d' % off_count, fortune)
    cache.set('fortune_%d' % all_count, fortune)

for fortune in enumerate(tame_fortunes):
    tame_count = cache.inc('tame_fortune_count')
    all_count = cache.inc('fortune_count')
    cache.set('tame_fortune_%d' % tame_count, fortune)
    cache.set('fortune_%d' % all_count, fortune)

from app import views
