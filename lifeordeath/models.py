from datetime import datetime
from collections import namedtuple
from momoko import BlockingClient

from settings import DATABASE


db = BlockingClient(DATABASE)


Stamp = namedtuple('Stamp', 'key, timestamp, frequency, warning')


def get(key=None):
    with db.connection as conn:
        cursor = conn.cursor()
        if key:
            cursor.execute('SELECT key, max(timestamp), frequency, warning '
                             'FROM stamp as s, event as e '
                             'WHERE s.event_id=e.id AND key=%s '
                             'GROUP BY key, frequency, warning;', (key,))
            result = cursor.fetchone()
            result = Stamp._make(result) if result else None
        else:
            cursor.execute('SELECT key, max(timestamp), frequency, warning '
                             'FROM stamp as s, event as e '
                             'WHERE s.event_id=e.id '
                             'GROUP BY key, frequency, warning;')
            result = map(Stamp._make, cursor.fetchall())
    return result


def update(key):
    updated = False
    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM event WHERE key=%s;', (key,))
        event = cursor.fetchone()
        if event:
            cursor.execute('INSERT INTO stamp (event_id, timestamp) '
                             'VALUES (%s, %s);', (event[0], datetime.now()))
            updated = True
    return updated
