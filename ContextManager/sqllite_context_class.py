import sqllite3


class SQLLite:
    """class to implement the Context Manager interface"""

    def __init__(self, filename: str):
        self.filename = filename
        self.connection = sqllite3.connect(filename)

    def __enter__(self):
        """called when the "with" block is entered"""
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, trace):
        """ " called when the "with" block is exited"""
        self.connection.commit()
        self.connection.close()


def main1():
    """test block"""
    with SQLLite(filename="application.db") as cursor:
        cursor.execute("SELECT * FROM blog")
        cursor.fetchall()
