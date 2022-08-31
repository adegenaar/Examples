"""
    Simple example of using pyodbc to make a database connection
"""
import pyodbc


def read(conn: pyodbc.Connection):
    """
    read

    Args:
        conn (Connection): the database connection
    """
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from dummy")
    for row in cursor:
        print(f"row={row}")
    print()


def insert(conn: pyodbc.Connection):
    """
    Create a record

    Args:
        conn (pyodbc.Connection): Database connection
    """
    print("create")
    cursor = conn.cursor()
    cursor.execute("insert into dummy(a,b) values(?,?);", (3232, "catsz"))
    conn.commit()
    read(conn)


def update(conn: pyodbc.Connection):
    """
    Update a record in the database

    Args:
        conn (pyodbc.Connection): Database connection
    """
    print("update")
    cursor = conn.cursor()
    cursor.execute("update dummy set b=? where a=?;", ("dogsz", 3232))
    conn.commit()
    read(conn)


def delete(conn: pyodbc.Connection):
    """
    delete a record from the database

    Args:
        conn (pyodbc.Connection): Database connection
    """
    print("delete")
    cursor = conn.cursor()
    cursor.execute("delete from dummy where a=?;", (3232))
    conn.commit()
    read(conn)


def create(conn: pyodbc.Connection):
    """
    create the table for the demo database

    Args:
        conn (pyodbc.Connection): Database connection object
    """
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE dummy (a int, b varchar(255));")
    conn.commit()


con = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};Server=.\SQLExpress;Database=;Trusted_Connection=yes;"
)

create(con)
read(con)
insert(con)
update(con)
delete(con)
