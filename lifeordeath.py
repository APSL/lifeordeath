import json

from tornado.web import Application, RequestHandler, HTTPError
from tornado.ioloop import IOLoop, PeriodicCallback

from models import get, update
from formats import geckoboard_rag_column
from settings import DEBUG, MONITOR


def encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


class MainHandler(RequestHandler):

    def get(self):
        stamps = get()
        self.write(json.dumps(stamps, default=encoder))
        self.finish()


class EventHandler(RequestHandler):

    def get(self, key):
        stamp = get(key)
        if not stamp:
            raise HTTPError(404)
        self.write(json.dumps(geckoboard_rag_column(stamp), default=encoder))
        self.finish()

    def post(self, key):
        if not update(key):
            raise HTTPError(404)
        self.finish()


def monitor():
    for stamp in get():
        print stamp.key, stamp.timestamp
    print


app = Application([
    (r"/", MainHandler),
    (r"/([\w-]+)/?", EventHandler),
], debug=DEBUG)


if __name__ == "__main__":
    app.listen(8888)
    PeriodicCallback(monitor, MONITOR).start()
    IOLoop.instance().start()
