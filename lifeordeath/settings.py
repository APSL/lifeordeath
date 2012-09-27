DEBUG = True

DATABASE = {
    'host': 'localhost',
    'database': 'lifeordeath',
    'user': 'jaime',
    'password': '',
    'min_conn': 1,
    'max_conn': 20,
    'cleanup_timeout': 10
}

MONITOR = 10 * 1000

FORMAT = 'formats.geckoboard.rag_column'

ALERT = 'alerts.stdout'
