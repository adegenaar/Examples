import pyodbc


def read(conn):
    print("Read")
    cursor = conn.cursor()
    cursor.execute("select * from dummy")
    for row in cursor:
        print(f'row={row}')
    print()

def create(conn):
    print("create")
    cursor=conn.cursor()
    cursor.execute('insert into dummy(a,b) values(?,?);',(3232,'catsz'))
    conn.commit()
    read(conn)

def update(conn):
    print("update")
    cursor=conn.cursor()
    cursor.execute('update dummy set b=? where a=?;',('dogsz',3232))
    conn.commit()
    read(conn)

def delete(conn):
    print("delete")
    cursor=conn.cursor()
    cursor.execute('delete from dummy where a=?;',(3232))
    conn.commit()
    read(conn)

conn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=;"
    "Database=;"
    "Trusted_Connection=yes;"
)

read(conn)
create(conn)
update(conn)
delete(conn)


