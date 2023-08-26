import psutil
import time

import pyodbc




# Variables to be used:
columns = ['cpu_fre','cpu_inter','cpu_percent','virtualMem_percent','available_memory','used_memory',]

DB_NAME = 'cpu_usage'

query_insert = """
  INSERT INTO cpu_data_table(cpu_fre,cpu_inter,cpu_percent,virtualMem_percent,available_memory,used_memory)
  VALUES(?, ?, ?, ?, ?, ?)
"""
query_db = f"CREATE DATABASE {DB_NAME}"

query_table = f"""
  CREATE TABLE cpu_data_table (
  Time datetime  default getdate() null,
  {columns[0]} int not null,
  {columns[1]} float not null,
  {columns[2]} int not null,
  {columns[3]} float not null,
  {columns[4]} float not null,
  {columns[5]} float not null
  )
"""

credentials = (
    r'Driver=SQL Server;'
    r'Server=.\SQLEXPRESS;'
    r'Trusted_Connection=yes;'
    r'Database=cpu_usage;'
    )


# Connect to SQL Server
def connection(credentials):
  conn = pyodbc.connect(credentials, autocommit=True)
  return conn



# #Create DB (Sql Server)
def create_db(query):
  db = cur.execute(query)
  print("DATABASE successfully created!")
  return db

#Create Table
def create_table(query):
  table = cur.execute(query)
  print("Table successfully created!")
  return table


# Import data from System performance to database
while True:
  conn = connection(credentials)
  cur = conn.cursor()

  cpu_fre = psutil.cpu_freq()[0]
  cpu_inter = round(psutil.cpu_stats()[1]/1000000,2)
  cpu_percent = psutil.cpu_percent()
  virtualMem_percent = psutil.virtual_memory()[2]
  available_memory = round(psutil.virtual_memory()[1]/1000000000,2)
  used_memory = round(psutil.virtual_memory()[3]/1000000000,2)

  # Insert data to database
  cur.execute(query_insert,(cpu_fre,cpu_inter,cpu_percent,virtualMem_percent,available_memory,used_memory))

  print("VALUES SUCCESSFULLY ADDED!")

  time.sleep(1)
  conn.close()







"Using MySQL Database"
# credentials = {
#   'host':'localhost',
#   'password':'chanchano123099',
#   'user':'root',
#   'database':'cpu_usage',
#   'auth_plugin':'mysql_native_password'
# }

# conn = mysql.connector.connect(**credentials)
# conn.autocommit = True
# cur = conn.cursor()

# #Create Database:

# def create_database(cursor):
#     try:
#         cursor.execute(
#             "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
#     except mysql.connector.Error as err:
#         print("Failed creating database: {}".format(err))
#         exit(1)

# try:
#     cur.execute("USE {}".format(DB_NAME))
# except mysql.connector.Error as err:
#     print("Database {} does not exists.".format(DB_NAME))
#     if err.errno == errorcode.ER_BAD_DB_ERROR:
#         create_database(cur)
#         print("Database {} created successfully.".format(DB_NAME))
#         conn.database = DB_NAME
#     else:
#         print(err)
#         exit(1)

# # #Create Table
# query_table_drop = "DROP TABLE IF EXISTS cpu_data_table"
# cur.execute(query_table_drop)
# query_table = f"""
#   CREATE TABLE IF NOT EXISTS cpu_data_table (
#   datetime timestamp null DEFAULT CURRENT_TIMESTAMP,
#   {columns[0]} int not null,
#   {columns[1]} float not null,
#   {columns[2]} int not null,
#   {columns[3]} float not null,
#   {columns[4]} float not null,
#   {columns[5]} float not null
#   )
# """
# cur.execute(query_table)

# print("Table successfully created!")

# conn.close()