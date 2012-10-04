from datetime import datetime, timedelta

import settings
from tornado.options import options as cfg
from util import silence_gap


def rag_column(stamp):
    data = dict(item=([dict(value=None, text=None)] * 3))

    now = datetime.now()
    frequency = cfg.events[stamp.key]['frequency']
    warning = cfg.events[stamp.key]['warning']

    if cfg.silence:
        start, end = silence_gap(now)
        if now >= start and stamp.timestamp < end:
            extra = (end - max(start, stamp.timestamp)).seconds
            frequency += extra
            warning += extra

    elapsed = now - stamp.timestamp
    if elapsed >= timedelta(seconds=frequency):
        colour = 0
    elif elapsed >= timedelta(seconds=warning):
        colour = 1
    else:
        colour = 2
    data['item'][colour] = {'value': elapsed.seconds / 60, 'text': 'mins ago'}
    return data
