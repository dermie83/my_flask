import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",              
  user="root",                   
  passwd="password1234",
    auth_plugin = 'mysql_native_password',
)


my_curser = my_db.cursor()

#my_curser.execute("CREATE DATABASE our_users")

my_curser.execute("SHOW DATABASES")
for db in my_curser:
    print(db)

