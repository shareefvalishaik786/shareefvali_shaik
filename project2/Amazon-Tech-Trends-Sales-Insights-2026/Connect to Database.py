import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5422",
    database="Project2"
)

cursor = conn.cursor()
print("MySQL Connected Successfully!")