import json

from datetime import datetime, timedelta
from tornado import gen
from tornado.web import Application, RequestHandler, asynchronous
from tornado.ioloop import IOLoop, PeriodicCallback

from models import get, update
from util import load_backend, encoder
from settings import ALERT, DEBUG, EVENTS, FORMAT, MONITOR


class MainHandler(RequestHandler):

    @asynchronous
    @gen.engine
    def get(self):
        stamps = yield gen.Task(get)
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


class EventHandler(RequestHandler):

    @asynchronous
    @gen.engine
    def get(self, key):
        if key not in EVENTS:
            self.send_error(404)
            return
        stamp = yield gen.Task(get, key)
        if not stamp:
            self.send_error(404)
            return
        event = EVENTS[stamp.key]
        self.write(json.dumps(format(stamp, event), default=encoder))
        self.finish()

    @asynchronous
    @gen.engine
    def post(self, key):
        if key not in EVENTS:
            self.send_error(404)
            return
        yield gen.Task(update, key)
        self.finish()


@gen.engine
def monitor():
    now = datetime.now()
    stamps = yield gen.Task(get)
    for stamp in stamps:
        if stamp.key in EVENTS:
            event = EVENTS[stamp.key]
            elapsed = now - stamp.timestamp
            if elapsed >= timedelta(seconds=event['frequency']):
                alert(stamp)


format = load_backend(FORMAT)
alert = load_backend(ALERT)

app = Application([
    (r"/", MainHandler),
    (r"/([\w-]+)/?", EventHandler),
], debug=DEBUG)


if __name__ == "__main__":
    app.listen(8888)
    PeriodicCallback(monitor, MONITOR).start()
    IOLoop.instance().start()
