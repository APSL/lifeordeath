from datetime import datetime
from collections import namedtuple

import tornado.ioloop
import tornado.web
import momoko
import json


EVERY = 60 * 1000


Stamp = namedtuple('Event', 'key, timestamp, frequency, ambar')


def dtencoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


db = momoko.BlockingClient({
    'host': 'localhost',
    'database': 'lifeordeath',
    'user': 'postgres',
    'password': 'postgres',
    'min_conn': 1,
    'max_conn': 20,
    'cleanup_timeout': 10
})


def get_all_last():
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT event_id, max(timestamp) FROM stamp GROUP BY event_id;')
        stamps = map(Stamp._make, cursor.fetchall())
    return stamps


def get_event(key):
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT key, max(timestamp), frequency, ambar FROM stamp as s, event as e WHERE s.event_id=s.id AND key=\'%s\' GROUP BY key, frequency, ambar;' % key)
        stamp = map(Stamp._make, cursor.fetchall())[0]
    return stamp


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        stamps = get_all_last()
        self.write(json.dumps(stamps, default=dtencoder))
        self.finish()


class EventHandler(tornado.web.RequestHandler):

    def get(self, key):
        stamp = get_event(key)
        self.write(json.dumps(stamp, default=dtencoder))
        self.finish()


class FixtureHandler(tornado.web.RequestHandler):

    def get(self):
        with db.connection as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO event (key, frequency, ambar) VALUES ('daily-digest', 60, 40);")
            cursor.execute("INSERT INTO event (key, frequency, ambar) VALUES ('backup', 120, 80);")
            cursor.execute("INSERT INTO stamp (event_id, timestamp) VALUES (1, '%s');" % datetime.now())
            cursor.execute("INSERT INTO stamp (event_id, timestamp) VALUES (1, '%s');" % datetime.now())
            cursor.execute("INSERT INTO stamp (event_id, timestamp) VALUES (2, '%s');" % datetime.now())
        self.finish()


next = {}


def monitor():
    for stamp in get_all_last():
        print stamp.key, stamp.timestamp
    print


app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/([\w-]+)/?", EventHandler),
    (r"/fixture", FixtureHandler),
], debug=True)


if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(monitor, EVERY).start()
    tornado.ioloop.IOLoop.instance().start()
