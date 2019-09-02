'''
Created on Sep 22, 2018

@author: Sauruk
'''
from Database import initializeLoginDB, custLogin, getNewCustNumber
import sqlite3

def addCustomer(db, username, password, secretKey = ''):
    c = db.cursor()
    sql = '''INSERT INTO loginInfo VALUES (?, ?, ?, ?)'''
    dataInsert = (getNewCustNumber(db), str(username), str(password), str(secretKey))
    c.execute(sql, dataInsert)
    db.commit()
    c.close()
    print ('Customer Added')

conn = initializeLoginDB()

print ("ADDING USER")
un = raw_input("Username: ")
pw = raw_input("password")

addCustomer(conn, un, pw)