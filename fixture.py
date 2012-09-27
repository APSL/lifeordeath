from models import db


if __name__ == "__main__":

    with db.connection as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO event (key, frequency, warning) VALUES ('daily-digest', 60, 40);")
        cursor.execute("INSERT INTO event (key, frequency, warning) VALUES ('backup', 120, 80);")
