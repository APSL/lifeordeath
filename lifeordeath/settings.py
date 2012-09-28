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

EVENTS = {
    'backup': {
        'frequency': 120,
        'warning': 40
    },
    'daily-digest': {
        'frequency': 60,
        'warning': 40
    }
}

MONITOR = 10 * 1000

FORMAT = 'formats.geckoboard.rag_column'

ALERT = 'alerts.stdout'
