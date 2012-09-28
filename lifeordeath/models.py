from functools import partial
from datetime import datetime
from collections import namedtuple
from momoko import AsyncClient

from settings import DATABASE


db = AsyncClient(DATABASE)


Stamp = namedtuple('Stamp', 'key, timestamp')


def on_stamp_got(callback, cursor):
    result = cursor.fetchone()
    stamp = Stamp._make(result) if result else None
    callback(stamp)


def on_stamps_got(callback, cursor):
    stamps = map(Stamp._make, cursor.fetchall())
    callback(stamps)


def get(key=None, callback=None):

    if key:
        db.execute('SELECT key, max(timestamp) FROM stamp WHERE key=%s GROUP BY key;', (key,),
                   callback=partial(on_stamp_got, callback))
    else:
        db.execute('SELECT key, max(timestamp) FROM stamp GROUP BY key;',
                   callback=partial(on_stamps_got, callback))


def on_stamp_updated(callback, cursor):
    callback()


def update(key, callback=None):

    db.execute('INSERT INTO stamp VALUES (%s, %s);', (key, datetime.now()),
               callback=partial(on_stamp_updated, callback))
