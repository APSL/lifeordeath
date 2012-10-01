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
    now = datetime.now()
    stamps = yield gen.Task(get, app)
    for stamp in stamps:
        if stamp.key in cfg.events:
            event = cfg.events[stamp.key]
            elapsed = now - stamp.timestamp
            if elapsed >= timedelta(seconds=event['frequency']):
                alert(stamp, **cfg.alert_options)


parse_config_file('/etc/lifeordeath.conf')
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
