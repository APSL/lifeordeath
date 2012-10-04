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
    frequency = cfg.events[stamp.key]['frequency']
    warning = cfg.events[stamp.key]['warning']

    if cfg.silence:
        if start is None or end is None:
            start, end = silence_gap(now)
        if now >= start and stamp.timestamp < end:
            extra = (end - max(start, stamp.timestamp)).seconds
            frequency += extra
            warning += extra

    return frequency, warning
