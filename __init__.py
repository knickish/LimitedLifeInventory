'''
Created on Sep 23, 2018

@author: Sauruk
'''

from Database import *
from TimeFormat import currTime
import sqlite3
import time
import traceback
import json
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getLoginInfo():
    userName = ""
    password = ""
    try:
        loginData = json.loads(request.data)
        loginData = loginData['message']
        print (loginData)
        userName = loginData['username']
        password = loginData['password']
        sessKey = addUserSession(userName, password)
        print (str(sessKey))
        return str(sessKey)
    except Exception:
        traceback.print_exc()
        return 'error, UserName: ' + userName + password
    
@app.route('/checkForSess/<int:sessKey>')
def checkForSess(sessKey):
    try:
        conn = initializeLoginDB()
        x = checkForExistingSess(conn, sessKey)
        return str(x)
    except Exception:
        traceback.print_exc()
        
    
@app.route('/hello')
def hello():
    return ("Can you hear me now?")
    


@app.route('/additem/<int:sessKey>', methods=['GET', 'POST'])
def addItem(sessKey):
    try:
        conn = initializeDb(getCustIdFromSessKey(sessKey))
        r = request.data
        itemData = json.loads(r) 
        print(itemData)
        try:
            itemData = itemData["message"]
        except Exception:
            traceback.print_exc() 
        print(itemData)
        uId = itemData['uId']
        itemNumber = itemData['itemNumber']
        initTime = currTime()
        creatorId = 0
        lifeTime = getLifetime(conn, int(itemNumber))
        x = addLabelToTable(conn, uId, itemNumber, lifeTime, initTime, creatorId)
        if x:
            print ('success')
        else:
            print('failure')
        return 'success'
    except Exception:
        traceback.print_exc()
        return 'error'
    
@app.route('/addtype/<int:sessKey>', methods=['GET', 'POST'])
def addItemType(sessKey):
    try:
        conn = initializeDb(getCustIdFromSessKey(sessKey))
        itemData = json.loads(request.data)
        print("Data for addtype: ")
        print (itemData)
        try:
            itemData = itemData['message']
        except Exception:
            traceback.print_exc() 
        try:
            itemNumber = getNewItemNumber(conn)
        except Exception:
            return 'error, already in database'
        itemName = itemData['itemName'].lower().capitalize()
        category = itemData['category'].lower().capitalize()
        lifetime = itemData['lifetime']
        x = -1;
        try:
            x = addItemToTable(conn, itemNumber, itemName, category, lifetime)
        except Exception:
            return 'failure'
        if x == 0:
            return 0
        return str(1)
    except Exception:
        traceback.print_exc()
        return str(2)

@app.route('/deleteType/<int:sessKey>', methods=['GET', 'POST'])
def delItemType(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    itemData = request.data
    x = delItemFromTable(conn, itemData)
    if x:
        return 'success'
    else:
        return'failure'
    
@app.route('/deleteItem/<int:uId>/<int:sessKey>', methods=['GET', 'POST'])
def delLabel(sessKey, uId):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    x = delLabelFromTable(conn, uId)
    if x:
        return 'success'
    else:
        return'failure'

@app.route('/getItem/<int:sessKey>', methods=['GET', 'POST'])
def getItem(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    itemData = request.data
    try:
        label = selLabelFromTable(conn, itemData)
    except Exception:
        return 'no such label'
    label = json.dumps(label.__dict__)
    return label

@app.route('/getItemType/<int:sessKey>', methods=['GET', 'POST'])
def getItemType(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    itemData = request.data
    try:
        item = selItemFromTable(conn, itemData)
    except Exception:
        return 'no such item'
    item = json.dumps(item.__dict__)
    return label

@app.route('/getItemsOfType/<int:sessKey>', methods=['GET', 'POST'])
def getItemsOfType(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    itemData = request.data
    z = getAllLablesOfType(conn, itemData)
    listOfLabels = []
    for j in range(len(z)):
        x = label(z[j][0], z[j][1], z[j][3], z[j][2], z[j][4])
        x = json.dumps(x.__dict__)
        listOfLabels.append(x)
    
    listOfLabels = json.dumps(listOfLabels)
    
@app.route('/getAllItems/<int:sessKey>')
def getAllItems(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    print ('1')
    z = selectAllLables(conn)
    print ('2')
    listOfLabels = []
    for j in range(len(z)):
        x = label(z[j][0], z[j][1], z[j][3], z[j][2], z[j][4])
        x = json.dumps(x.__dict__)
        listOfLabels.append(x)
        print ('in loop')
    listOfLabels = json.dumps(listOfLabels)
    return listOfLabels
    
@app.route('/getAllItemTypes/<int:sessKey>')
def getItemTypes(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    z = selectAllItems(conn)
    listOfItems = []
    print (z)
    for j in range(len(z)):
        x = item(z[j][1], z[j][0], z[j][2], z[j][3])
        x = x.__dict__
        listOfItems.append(x)
    listOfItems = json.dumps(listOfItems)
    return listOfItems
    
@app.route('/getAllByCat/<int:sessKey>')
def getAllByCat(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    returnVar = selectAllItemsByCategory(conn)
    return returnVar
    
@app.route('/getNumberXNameMap/<int:sessKey>')  
def getNumberXNameMap(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    x = getNumberNameMap(conn)
    return x
    
@app.route('/getCats/<int:sessKey>')
def getCats(sessKey):
    conn = initializeDb(getCustIdFromSessKey(sessKey))
    return getCategories(conn)
    
        
if __name__ == '__main__':
    app.run(debug=True)