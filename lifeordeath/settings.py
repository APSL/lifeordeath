from tornado.options import define


define('debug', default=True)
define('port', default=8888)
define('monitor', default=60 * 1000)
define('format', default='formats.geckoboard.rag_column')
define('alert', default='alerts.stdout')
define('events', default={})
define('database', default={
    'host': 'localhost',
    'database': 'lifeordeath',
    'user': 'lifeordeath',
    'password': '',
    'min_conn': 1,
    'max_conn': 20,
    'cleanup_timeout': 10
})
