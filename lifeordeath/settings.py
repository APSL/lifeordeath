from tornado.options import define


# This is the settings definition. Do not edit this file.
# To customize yor settings, you can override the default
# values via /etc/lifeordeath or via command-line arguments.

define('debug', default=False)
define('port', default=8888)
define('auth_user', default=None)
define('auth_pass', default=None)
define('monitor', default=60 * 1000)
define('silence', default='')
define('format', default='formats.geckoboard.rag_column')
define('alert', default='alerts.stdout')
define('alert_options', default={})
define('alert_duration', default=None)
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
