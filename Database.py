
import sqlite3
import random
from TimeFormat import currTime
from math import floor
import traceback
import json
import platform

__all__ = ['checkForExistingSess', 'getCategories', 'getNumberNameMap', 'selectAllItemsByCategory', 'selectAllItems', 'selectAllLables', 'selItemFromTable', 'getCustIdFromSessKey', 'addUserSession', 'getNewCustNumber', 'initializeLoginDB', 'printAllItems', 'printAllLablesOfType', 'getAllLablesOfType', 'getNewItemNumber', 'initializeDb', 'addItemToTable', 'addEmpToTable', 'addLabelToTable', 'delItemFromTable', 'delEmpFromTable', 'delLabelFromTable', 'findItemNumber', 'getLifetime', 'selLabelFromTable', "itemCounter", "item", "label"]

class itemCounter:
    nexId= 1
    listOfEmpties = []
    
    def __init__(self, recovered = 1):
        self.nextId = recovered
        
    def incNext(self):
        self.nextId = self.nextId+1
        
    def addToEmptyList(self, deprecatedNumber):
        if deprecatedNumber not in self.listOfEmpties:
            self.listOfEmpties.append(deprecatedNumber)
        
    def removeEmpty(self, number):
        if number in self.listOfEmpties:
            self.listOfEmpties.remove(number)
        
    def getUid(self):
        if not self.listOfEmpties:
            returnVal = self.nextId
            self.incNext()
            return returnVal
        else:
            returnVal = self.listOfEmpties[0]
            self.removeEmpty(returnVal)
            return returnVal

class item:
    itemName = 'name'
    itemNumber = 1234
    category = ''
    lifetime = 12345
    
    
    def __init__(self, name, itemNumber, category, lifetime):
        self.itemName = name.lower().capitalize()
        self.itemNumber = itemNumber
        self.category = category.lower().capitalize()
        self.lifetime = lifetime
    
    def printItem(self):
        lifeRemaining = self.lifetime
        lifeMonths = lifeRemaining / 720
        lifeRemaining = lifeRemaining % 720
        lifeDays = lifeRemaining / 24
        lifeRemaining = lifeRemaining % 24
        print ("%s - Lifetime: %s Months, %s Days, and %s Hours") % ((self.itemName).capitalize(), int(lifeMonths), int(lifeDays), int(lifeRemaining))
        
        
class label:
    uid = 123 #must be unique
    itemNumber = 123 # must exist in items database
    lifetime = 1234 #stored in hours
    initTime = 1234 #stored in epoch time (minutes) to deal with short-lifetime items
    creatorId = 12
    itemNotes = {}
    
    def __init__(self, uId, itemNumber, initTime, lifeTime, creatorId, note = ''):
        self.uid = uId
        self.itemNumber = itemNumber
        self.initTime = initTime
        self.creatorId = creatorId
        self.lifetime = lifeTime
        self.itemNotes[0] = note 
    
    def printLabel(self, db):
        name = findItemName(db, self.itemNumber)
        lifeRemaining = self.getLifeRemaining()
        lifeMonths = lifeRemaining / 720
        lifeRemaining = lifeRemaining % 720
        lifeDays = lifeRemaining / 24
        lifeRemaining = lifeRemaining % 24
        print ("%s : %s Expires in %s Months, %s Days, and %s Hours") % (int(self.uid), name, floor(lifeMonths), floor(lifeDays), floor(lifeRemaining))
    
    def addNote(self, note):
        self.itemNotes[len(self.itemNotes)] = note


    def getLifeRemaining (self):
        lifeRemaining = ((60*self.lifetime) - int(currTime()-(self.initTime)))/60
        return lifeRemaining
    

def initializeLoginDB():
    if (platform.system() != "Windows"):
        dbNameString = './loginInfo.db'
    if (platform.system() == "Windows"):
        dbNameString = 'loginInfo.db'
    
    conn = sqlite3.connect(dbNameString)
    c = conn.cursor()
    dbExists = c.execute('''select count(*) from sqlite_master where type='table' and name='loginInfo';''').fetchone()
    dbExists = dbExists[0]
    if not dbExists:
        print("Creating AddUser table")
        c.execute('''CREATE TABLE IF NOT EXISTS loginInfo
                    (customerId real PRIMARY KEY,
                    screenName text,
                    password text,
                    secretKey text);''')
        c.execute('''CREATE TABLE IF NOT EXISTS loginSessions
                    (sessionKey real PRIMARY KEY,
                    customerId real,
                    createDate real);''')
        conn.commit()
        try:
            c.execute('''INSERT INTO loginInfo VALUES (1, 'admin', 'admin', '0');''' )
            conn.commit()
        except Exception:
            print('admin login already exists')
            traceback.print_exc()
    c.close()
    return conn

def checkForExistingSess(db, sessKey):
    if(type(db)!=sqlite3.Cursor):
        db = db.cursor()
    sql = '''SELECT count(*) FROM loginSessions WHERE sessionKey = ?'''
    dataInsert = (sessKey,)
    x = db.execute(sql, dataInsert).fetchone()[0]
    print(x)
    return x

def addUserSession(email, password):
    conn = initializeLoginDB()
    c = conn.cursor()
    dataInsert = (str(email), str(password))
    sql = '''SELECT * FROM loginInfo WHERE screenName = ? AND password = ?'''
    row = c.execute(sql, dataInsert).fetchone()
    try:
        x = 1
        custID = row[0]
        while x==1:
            sessKey = random.randint(10000,10000000)
            x = checkForExistingSess(c, sessKey)
        sql = '''INSERT INTO loginSessions VALUES (?, ?, ?);'''
        dataInsert = (sessKey, custID, currTime())
        c.execute(sql, dataInsert)
        conn.commit()
        c.close()
        return sessKey
    except KeyError:
        c.close()
        addUserSession(email, password)
    except Exception:
        traceback.print_exc()
        c.close()
        return 0;
    
def getCustIdFromSessKey (sessKey):
    conn = initializeLoginDB()
    c = conn.cursor()
    sql = '''SELECT customerID FROM loginSessions WHERE sessionKey = ?;'''
    dataInsert = (int(sessKey),)
    r = c.execute(sql, dataInsert).fetchone()
    try:
        custId = r[0]
        c.close()
        print ('customerID retrieved')
        return custId
    except Exception:
        traceback.print_exc()
        c.close()
        return 0;

    
def initializeDb(custId):
    if (platform.system() != "Windows"):
        dbNameString = '/var/www/FlaskApp/FlaskApp/dataStorage'
    if (platform.system() == "Windows"):
        dbNameString = 'dataStorage'
    
    dbNameString += str(int(custId)) +'.db'
    conn = sqlite3.connect(dbNameString)
    c = conn.cursor()
    #create table
    dbExists = c.execute('''select count(*) from sqlite_master where type='table' and name='employees';''').fetchone()
    dbExists = dbExists[0]
    if not dbExists:
        print("Creating tables")
        c.execute('''CREATE TABLE items
                    (itemNumber real PRIMARY KEY, 
                    itemName text,
                    category text, 
                    lifeTime real
                    );''')
        c.execute('''CREATE TABLE labels
                    (uId real PRIMARY KEY, 
                    itemNumber real, 
                    itemlifetime real, 
                    itemCreateDate real, 
                    creatorId real
                    );''')
        c.execute('''CREATE TABLE employees
                    (employeeId real PRIMARY KEY, 
                    employeeName text,
                    employeePW text, 
                    employeePrivLevel real
                    );''') 
        addEmpToTable(conn, 1, 'admin', 'admin', 3)
    c.close()
    print ('table created')
    return conn   

def addItemToTable(db, itemNumber, itemName, category, lifeTime):
    c = db.cursor()
    sql = '''SELECT * FROM items WHERE itemNumber = ?'''
    testVar = c.execute(sql, (itemNumber,)).fetchone()
    if testVar:
        print("Already In Database")
        c.close()
        return 0;
    sql = '''INSERT INTO items (itemNumber, itemName, category, lifeTime)''' '''VALUES (?, ?, ?, ?)'''
    dataInsert = (itemNumber, itemName, category, lifeTime)
    c.execute(sql, dataInsert)
    db.commit()
    print("1 record inserted, ID: " + str(int(c.lastrowid)))
    c.close()
    
def addLabelToTable(db, uId, itemNumber, itemlifetime, itemCreateDate, creatorId):
    c = db.cursor()
    sql = '''SELECT count(*) FROM labels WHERE uId = ?'''
    testVar = c.execute(sql, (uId,)).fetchone()[0]
    print (testVar)
    if testVar:
        print("Already In Database")
        c.close()
        return 0;
    else:
        sql = '''INSERT INTO labels VALUES(?, ?, ?, ?, ?)'''
        dataInsert = (uId, itemNumber, itemlifetime, itemCreateDate, creatorId)
        c.execute(sql, dataInsert)
        db.commit() 
        c.close()
        return 1;
    
def addEmpToTable(db, employeeId, employeeName, employeePW, employeePrivLevel):
    c = db.cursor()
    sql = "INSERT INTO employees VALUES(?, ?, ?, ?)"
    dataInsert = (employeeId, employeeName, employeePW, employeePrivLevel)
    c.execute(sql, dataInsert)
    db.commit()
    c.close()
    print("1 record inserted, ID:", c.lastrowid) 
    
def checkIfSessKey(db, sessKey):
    c = db.cursor()
    sql = "SELECT count(*) FROM logim)"
    dataInsert = (sessKey)
    c.execute(sql, dataInsert)
    
    
def delItemFromTable(db, itemNumber):
    c = db.cursor()
    sql = "DELETE FROM items WHERE itemNumber = ?"
    delVal = (itemNumber)
    c.execute(sql, (delVal,))
    print("Deleted lable number: "+ itemNumber)
    db.commit()
    c.close()
    
    
def delLabelFromTable(db, uId):
    c = db.cursor()
    sql = "DELETE FROM labels WHERE uId = ?"
    delVal = (uId)
    c.execute(sql, (delVal,))
    db.commit()
    c.close()
    
def delEmpFromTable(db, empId):
    c = db.cursor()
    sql = '''DELETE FROM employees WHERE employeeId = ?'''
    delVal = (empId)
    c.execute(sql, (delVal,))
    db.commit()
    c.close()
    
def getNewItemNumber(db):
    c = db.cursor()
    sql = '''SELECT itemNumber FROM items'''
    itemNumbersTuple = c.execute(sql).fetchall()
    listOfItemNumbers = []
    for x in itemNumbersTuple:
        listOfItemNumbers.append(int(x[0]))
    listOfItemNumbers.sort()
    x = 0 
    y = 1
    try:
        while (y == int(listOfItemNumbers[x])):
            x+=1
            y+=1
    except Exception:
        pass
    return y

def getNewEmpNumber(db):
    c = db.cursor()
    sql = '''SELECT empID FROM employees'''
    empNumbersTuple = c.execute(sql).fetchall()
    listOfEmpNumbers = []
    for x in empNumbersTuple:
        listOfEmpNumbers.append(int(x[0]))
    listOfEmpNumbers.sort()
    x = 0 
    y = 1
    try:
        while (y == int(listOfEmpNumbers[x])):
            x+=1
            y+=1
    except Exception:
        pass
    return y

def getNewCustNumber(db):
    c = db.cursor()
    sql = '''SELECT customerID FROM loginInfo'''
    empNumbersTuple = c.execute(sql).fetchall()
    listOfEmpNumbers = []
    for x in empNumbersTuple:
        listOfEmpNumbers.append(int(x[0]))
    listOfEmpNumbers.sort()
    x = 0 
    y = 1
    try:
        while (y == int(listOfEmpNumbers[x])):
            x+=1
            y+=1
    except Exception:
        pass
    return y
 
    
def selLabelFromTable(db, itemNumber):
    c = db.cursor()
    sql = "SELECT * FROM labels WHERE uId = ?"
    selVal = (str(itemNumber),)
    c.execute(sql, selVal)
    row = c.fetchone()
    x = label(row[0], row[1], row[3], row[2],row[4])
    c.close()
    return x
    
def selItemFromTable(db, itemNumber):
    c = db.cursor()
    sql = "SELECT * FROM items WHERE itemNumber = ?"
    selVal = (itemNumber,)
    row = c.execute(sql, selVal).fetchone()
    x = item(row[1], row[0], row[2])
    c.close()
    return x
    
def selEmployeeFromTable(db, itemNumber):
    c = db.cursor()
    sql = "SELECT FROM items WHERE itemNumber = ?"
    delVal = (itemNumber)
    c.execute(sql, (delVal,))
    db.commit()
    c.close()
    
def findItemNumber(db, stringArg):
    c = db.cursor()
    name = stringArg
    sql = '''SELECT itemNumber FROM items WHERE itemName = ?'''
    returnVal = c.execute(sql, (name,)).fetchone()
    if returnVal:
        c.close()
        return returnVal[0]
    else:
        c.close()
        return 0;
    
def findItemName(db, itemNumber):
    c = db.cursor()
    sql = '''SELECT itemName FROM items WHERE itemNumber = ?'''
    returnVal = c.execute(sql, (itemNumber,)).fetchone()
    if returnVal:
        returnVal = (returnVal[0]).capitalize()
        c.close()
        return returnVal
    else:
        c.close()
        return 0;
    
def getLifetime(db, itemNo):
    c = db.cursor()
    sql = '''SELECT lifetime FROM items WHERE itemNumber = ?'''
    try:
        returnVal = c.execute(sql, (itemNo,)).fetchone()[0]
    except Exception:
        traceback.print_exc()
        c.close()
        pass
    if returnVal:
        c.close()
        return returnVal
    else:
        c.close()
        return 0;
    
def getAllLablesOfType(db, itemNumber):
    c = db.cursor()
    sql = '''SELECT * FROM labels WHERE itemNumber = ?'''
    listOfLabels = c.execute(sql, (itemNumber,)).fetchall()
    c.close()
    return listOfLabels

def printAllLablesOfType(db, itemNumber):
    c=db.cursor()
    sql = '''SELECT uId FROM labels WHERE itemNumber = ?'''
    labelNumList = c.execute(sql, (itemNumber,)).fetchall()
    for z in labelNumList:
        label = selLabelFromTable(db, z[0])
        label.printLabel(db)
    c.close()
    
def selectAllLables(db):
    c = db.cursor()
    sql = '''SELECT * FROM labels'''
    listOfLabels = c.execute(sql).fetchall()
    c.close()
    return listOfLabels

def selectAllItems(db):
    c = db.cursor()
    sql = '''SELECT * FROM items'''
    listOfItems = c.execute(sql).fetchall()
    c.close()
    return listOfItems

def printAllItems(db):
    c=db.cursor()
    sql = '''SELECT itemNumber FROM items'''
    itemsNums = c.execute(sql).fetchall()
    for x in itemsNums:
        item = selItemFromTable(db, x[0])
        item.printItem()
    c.close()
    
    
def selectAllItemsByCategory(db):
    c = db.cursor()
    sql = '''SELECT category FROM items'''
    listOfItems = c.execute(sql).fetchall()
    categoryList = []
    jsonItemList = []
    for x in listOfItems:
        if str(x[0]) not in categoryList:
            categoryList.append(str(x[0]))
    for x in categoryList:
        sql = '''SELECT itemNumber from items WHERE category = ?'''
        z = c.execute(sql, (x,)).fetchall()
        listOfItemTypesforCategory = []
        for i in z:
            listOfItemTypesforCategory.append(i)
        listOfLabels = []
        for j in listOfItemTypesforCategory:
            sql = '''SELECT * from labels WHERE itemNumber = ?;'''
            r = c.execute(sql, j).fetchall()
            for i in r:
                t = label(i[0], i[1], i[3], i[2], i[4])
                t = t.__dict__
                listOfLabels.append(t)
        pairDict = {}
        pairDict[x] = listOfLabels
        jsonItemList.append(pairDict)
    jsonItemList = json.dumps(jsonItemList)
    c.close()
    return jsonItemList

def getNumberNameMap(db):
    c = db.cursor()
    sql = '''SELECT itemNumber, itemName FROM items'''
    selection = c.execute(sql).fetchall()
    selection = json.dumps(selection)
    return selection

def getCategories(db):
    c = db.cursor()
    sql = '''SELECT category FROM items'''
    row = c.execute(sql).fetchall()
    listOfCats = []
    for x in row:
        if x[0] not in listOfCats:
            listOfCats.append(x[0])
    listOfCats = json.dumps(listOfCats)
    return listOfCats
    