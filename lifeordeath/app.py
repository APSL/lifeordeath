import json

from datetime import datetime, timedelta
from tornado.web import Application, RequestHandler, asynchronous
from tornado.ioloop import IOLoop, PeriodicCallback

from models import get, update
from util import load_backend, encoder
from settings import ALERT, DEBUG, EVENTS, FORMAT, MONITOR


class MainHandler(RequestHandler):

    @asynchronous
    def get(self):
        get(callback=self.on_stamps_got)

    def on_stamps_got(self, stamps):
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


class EventHandler(RequestHandler):

    @asynchronous
    def get(self, key):
        if key not in EVENTS:
            self.send_error(404)
            return
        get(key, callback=self.on_stamp_got)

    def on_stamp_got(self, stamp):
        if not stamp:
            self.send_error(404)
            return
        event = EVENTS[stamp.key]
        self.write(json.dumps(format(stamp, event), default=encoder))
        self.finish()

    @asynchronous
    def post(self, key):
        if key not in EVENTS:
            self.send_error(404)
            return
        update(key, callback=self.on_stamp_updated)

    def on_stamp_updated(self):
        self.finish()


def monitor():
    get(callback=on_stamps_got)


def on_stamps_got(stamps):
    now = datetime.now()
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
