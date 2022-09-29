import pymysql

mydb = pymysql.connect(host="localhost",user="root",password="")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE accounts")
mydb.close()

mydb = pymysql.connect(host="localhost",user="root",password="",database="accounts")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE accounts (username_info VARCHAR(1000), password_hash VARCHAR(1000))")
mydb.close()

print("Success...")