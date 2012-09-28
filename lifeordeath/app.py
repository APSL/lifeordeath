import json

from datetime import datetime, timedelta
from tornado.web import Application, RequestHandler, HTTPError
from tornado.ioloop import IOLoop, PeriodicCallback

from models import get, update
from util import load_backend, encoder
from settings import ALERT, DEBUG, EVENTS, FORMAT, MONITOR


class MainHandler(RequestHandler):

    def get(self):
        stamps = get()
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


class EventHandler(RequestHandler):

    def get(self, key):
        event = EVENTS.get(key)
        if not event:
            raise HTTPError(404)
        stamp = get(key)
        if not stamp:
            raise HTTPError(404)
        self.write(json.dumps(format(stamp, event), default=encoder))
        self.finish()

    def post(self, key):
        if key not in EVENTS:
            raise HTTPError(404)
        update(key)
        self.finish()


def monitor():
    now = datetime.now()
    for stamp in get():
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
