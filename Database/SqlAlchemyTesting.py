# in order to run this test you will need to install pyodbc, sqlalchemy and pandas 
# for more details see: https://overiq.com/sqlalchemy-101/intro-to-sqlalchemy/
# for connecting to an existing database: https://stackoverflow.com/questions/39955521/sqlalchemy-existing-database-query

import pyodbc
import sqlalchemy
#from sqlalchemy import create_engine
import pandas as pd

# in order to connect, we need server name, database name we want to connect to
# the general format is: 
#   dialect+driver://username:password@host:port/database
engine = sqlalchemy.create_engine('mssql+pyodbc://server_name/database_name?driver=SQL Server?Trusted_Connection=yes')

# server_name : server you want to connect to
# database_name : database you want to work with
# Trusted_Connection = yes, when using windows authentication. 
# If you have set a separate username and password for your SQL database,
#   sal.create_engine(‘dialect+driver://username:password@host:port/database’)

# establishing the connection to the databse using engine as an interface
conn = engine.connect()

# printing names of the tables present in the database
print(engine.table_names())

# checking whether the connection was actually established by selecting and displaying contents of table from the database
result = engine.execute("select * from tablename")
for row in result:
    print (row)
result.close()

# reading a SQL query using pandas
sql_query = pd.read_sql_query('SELECT * FROM database_name.dbo.tablename', engine)
# saving SQL table in a pandas data frame
df = pd.DataFrame(sql_query, columns = ['column1','column2'])
# printing the dataframe
df

#Reading an external file and storing it to a SQL table
#We can read a CSV, excel file and store its content to a SQL table.
df = pd.read_csv('tablename')
# create a new table and append data frame values to this table
df.to_sql('tablename', con=engine, if_exists='append',index=False,chunksize=1000)

#Closing the connection
conn.close()