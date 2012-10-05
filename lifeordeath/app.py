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
from util import load_backend, encoder, silence_gap, thresholds, require_basic_auth


CONFIG = '/etc/lifeordeath.conf'


@require_basic_auth
class MainHandler(RequestHandler):

    @asynchronous
    @gen.engine
    def get(self):
        stamps = yield gen.Task(get, app)
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


@require_basic_auth
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
        now = datetime.now()
        frequency, warning = thresholds(stamp, now)
        elapsed = now - stamp.timestamp
        data = format(stamp, frequency, warning, elapsed)
        self.write(json.dumps(data, default=encoder))
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
        start, end = silence_gap(now)
        if start <= now <= end:
            return

    for stamp in stamps:
        if stamp.key in cfg.events:
            frequency, _ = thresholds(stamp, now, start, end)
            elapsed = now - stamp.timestamp
            if elapsed >= timedelta(seconds=frequency):
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
