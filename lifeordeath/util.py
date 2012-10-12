import settings
from tornado.options import options as cfg


#
# import_module() from Python 2.7
#

import sys


def _resolve_name(name, package, level):
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

### end of import_module()


def load_backend(path):
    module, func = path.rsplit('.', 1)
    module = import_module(module)
    return getattr(module, func)


def encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


def silence_gap(now):
    start, end = cfg.silence.split('-')
    shour, smin = map(int, start.split(':'))
    ehour, emin = map(int, end.split(':'))
    start = now.replace(hour=shour, minute=smin, second=0, microsecond=0)
    end = now.replace(hour=ehour, minute=emin, second=0, microsecond=0)
    return start, end


def thresholds(stamp, now, start=None, end=None):
    error = cfg.events[stamp.key]['error']
    warning = cfg.events[stamp.key]['warning']

    if cfg.silence:
        if start is None or end is None:
            start, end = silence_gap(now)
        if now >= start and stamp.timestamp < end:
            extra = (min(end, now) - max(start, stamp.timestamp)).seconds
            error += extra
            warning += extra

    return error, warning


#
# Basic HTTP auth decorator based on:
# http://kelleyk.com/post/7362319243/easy-basic-http-authentication-with-tornado
#

import base64

def require_basic_auth(handler_class):
    def wrap_execute(handler_execute):
        def _execute(self, transforms, *args, **kwargs):
            if not cfg.debug and cfg.auth_user and cfg.auth_pass:
                auth_header = self.request.headers.get('Authorization')
                if auth_header is None or not auth_header.startswith('Basic '):
                    self.set_status(401)
                    self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                    self._transforms = []
                    self.finish()
                    return False
                auth_decoded = base64.decodestring(auth_header[6:])
                user, password = auth_decoded.split(':', 2)
                if user != cfg.auth_user or password != cfg.auth_pass:
                    self.set_status(401)
                    self._transforms = []
                    self.finish()
                    return False
            return handler_execute(self, transforms, *args, **kwargs)
        return _execute
    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class
