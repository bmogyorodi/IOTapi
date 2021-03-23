import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Reader",
  password="password"
)

print(mydb)