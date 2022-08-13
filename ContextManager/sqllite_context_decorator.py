import sqllite3
from contextlib import contextmanager


@contextmanager
def open_db(filename: str):
    connection = sqllite3.connect(filename)
    try:
        cursor = connection.cursor()
        yield cursor
    finally:
        connection.commit()
        connection.close()


def main():
    with open_db(filename="application.db") as cursor:
        cursor.execute("SELECT * FROM blog")
        cursor.fetchall()
