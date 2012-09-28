from datetime import datetime
from collections import namedtuple
from momoko import BlockingClient

from settings import DATABASE


db = BlockingClient(DATABASE)


Stamp = namedtuple('Stamp', 'key, timestamp')


def get(key=None):
    with db.connection as conn:
        cursor = conn.cursor()
        if key:
            cursor.execute('SELECT key, max(timestamp) FROM stamp WHERE key=%s GROUP BY key;', (key,))
            result = cursor.fetchone()
            result = Stamp._make(result) if result else None
        else:
            cursor.execute('SELECT key, max(timestamp) FROM stamp GROUP BY key;')
            result = map(Stamp._make, cursor.fetchall())
    return result


def update(key):
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO stamp VALUES (%s, %s);', (key, datetime.now()))
