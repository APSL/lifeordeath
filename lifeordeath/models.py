from functools import partial
from collections import namedtuple


Stamp = namedtuple('Stamp', 'key, timestamp')


def get(app, key=None, callback=None):

    def on_stamp_got(callback, cursor):
        result = cursor.fetchone()
        stamp = Stamp._make(result) if result else None
        callback(stamp)

    def on_stamps_got(callback, cursor):
        stamps = map(Stamp._make, cursor.fetchall())
        callback(stamps)

    if key:
        app.db.execute('SELECT key, max(timestamp) FROM stamp WHERE key=%s GROUP BY key;', (key,),
                       callback=partial(on_stamp_got, callback))
    else:
        app.db.execute('SELECT key, max(timestamp) FROM stamp GROUP BY key;',
                       callback=partial(on_stamps_got, callback))


def update(app, key, callback=None):

    def on_stamp_updated(callback, cursor):
        callback()

    app.db.transaction((
      ('UPDATE stamp set timestamp=current_timestamp WHERE key=%s;', (key,)),
      ('INSERT INTO stamp (key, timestamp) '
              'SELECT %s, current_timestamp '
              'WHERE NOT EXISTS (SELECT 1 FROM stamp WHERE key=%s);'), (key, key)),
      callback=partial(on_stamp_updated, callback))
