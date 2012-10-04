import os
import json

from datetime import datetime, timedelta
from momoko import AsyncClient
from tornado import gen
from tornado.web import Application, RequestHandler, asynchronous
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import parse_config_file, parse_command_line

import settings
from tornado.options import options as cfg
from models import get, update
from util import load_backend, encoder


CONFIG = '/etc/lifeordeath.conf'


class MainHandler(RequestHandler):

    @asynchronous
    @gen.engine
    def get(self):
        stamps = yield gen.Task(get, app)
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


class EventHandler(RequestHandler):

    @asynchronous
    @gen.engine
    def get(self, key):
        if key not in cfg.events:
            self.send_error(404)
            return
        stamp = yield gen.Task(get, app, key)
        if not stamp:
            self.send_error(404)
            return
        event = cfg.events[stamp.key]
        self.write(json.dumps(format(stamp, event), default=encoder))
        self.finish()

    @asynchronous
    @gen.engine
    def post(self, key):
        if key not in cfg.events:
            self.send_error(404)
            return
        yield gen.Task(update, app, key)
        self.finish()


@gen.engine
def monitor():
    stamps = yield gen.Task(get, app)
    if not stamps:
        return

    now = datetime.now()

    if cfg.silence:
        start, end = cfg.silence.split('-')
        shour, smin = map(int, start.split(':'))
        ehour, emin = map(int, end.split(':'))
        start = now.replace(hour=shour, minute=smin, second=0, microsecond=0)
        end = now.replace(hour=ehour, minute=emin, second=0, microsecond=0)
        if start <= now <= end:
            return

    for stamp in stamps:
        if stamp.key in cfg.events:
            threshold = cfg.events[stamp.key]['frequency']
            if cfg.silence and now > end and stamp.timestamp < end:
                threshold += (end - max(start, stamp.timestamp)).seconds
            elapsed = now - stamp.timestamp
            if elapsed >= timedelta(seconds=threshold):
                alert(stamp, **cfg.alert_options)


if os.path.exists(CONFIG):
    parse_config_file(CONFIG)
parse_command_line()

format = load_backend(cfg.format)
alert = load_backend(cfg.alert)

app = Application([
    (r"/", MainHandler),
    (r"/([\w-]+)/?", EventHandler),
], debug=cfg.debug)

app.db = AsyncClient(cfg.database)

app.listen(cfg.port)
PeriodicCallback(monitor, cfg.monitor).start()
IOLoop.instance().start()
