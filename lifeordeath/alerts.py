from urllib import urlencode
from tornado.httpclient import AsyncHTTPClient

import settings
from tornado.options import options as cfg


def stdout(stamp):
    print stamp.key, stamp.timestamp


def sentry(stamp):
    server = 'test' if cfg.debug else 'www'
    level = 'info' if cfg.debug else 'fatal'
    message = 'lifeordeath alert: %s' % stamp.key
    url = 'https://%s.streetlife.com/sentry-endpoint/?key=str33tl1f3s3ntry' % server
    args = {'logger_name': 'general', 'level': level, 'message': message}
    http = AsyncHTTPClient()
    http.fetch(url, method='POST', body=urlencode(args), callback=None)
