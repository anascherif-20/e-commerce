import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce"
)

cursor = db.cursor(dictionary=True)
