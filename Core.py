'''
Created on Sep 15, 2018

@author: Sauruk
'''

from Database import *
from TimeFormat import currTime
import sqlite3
import time
import traceback


def runInterface(empIdNo = 0, custIdNumber = 0):
    
    custNo = custIdNumber
    if not custNo:
        custNo = login()
    conn = initializeDb(custNo)
    c = conn.cursor()
    c.execute("PRAGMA busy_timeout = 10000")
    c.close()

    empId = empIdNo
    
    if not empId:
        empId = input("What is your ID number? ")
    else:
        pass


    pathSelector = input("1: Add Item, 2: Delete Item, 3: View Item, 4: View All Items, 5: View All Items Of Type 6: Admin, 7: Exit ")
    
    if pathSelector == 1:
        name = raw_input("Food Type? ")
        name = name.lower()
        try:
            itemNumber = int(findItemNumber(conn, name))
            itemLife = int(getLifetime(conn, itemNumber))
            uId = input("Label Number?")
            time = currTime()
            x = addLabelToTable(conn, uId, itemNumber, itemLife, time, empId)
            if not x:
                print ("Failure")
            else:
                print ("Item Added")
        except Exception:
            print("Food type not in database. Add food type from Admin menu.")
        
    if pathSelector == 2:
        labelNo = input("Enter label number to delete: ")
        delLabelFromTable(conn, labelNo)
        
        
    if pathSelector == 3:
        try:  
            labelNo = input("Enter label number to view: ")
            label = selLabelFromTable(conn, labelNo)
            label.printLabel(conn)
        except Exception:
            print ("Label Number Not In Database")
        
    if pathSelector == 4:
        printAllLables(conn)
        
    if pathSelector == 5:
        name = raw_input("Food Type? ")
        name = name.lower()
        try:
            itemNumber = int(findItemNumber(conn, name))
        except Exception:
            print("Food type not in database. Add food type from Admin menu.")
        printAllLablesOfType(conn, itemNumber)
    
    
    if pathSelector == 6:
        pathSelector = input("1: Add New Food Type, 2: Delete Food Type, 3: List All Food Types 4: Add Employee, 5: Remove Employee, 5: Back ")
        if pathSelector == 1:
            name = raw_input("Food Type? ")
            name = name.lower()
            itemLife = 0
            itemLife += 720*input("Enter number of months for which this item can be kept: ")
            itemLife += 24*input("Enter number of days for which this item can be kept: ")
            itemLife += input("Enter number of hours for which this item can be kept: ")
            print (itemLife)
            itemLife = int(itemLife)
            x = item(name, getNewItemNumber(conn), itemLife)
            itemId = x.itemNumber
            addItemToTable(conn, itemId, name, itemLife)
            
        
        if pathSelector == 2:
            stringArg = raw_input("Enter the name of the food type you would like to delete: ")
            stringArg = stringArg.lower()
            itemNum = findItemNumber(conn, stringArg)
            delItemFromTable(conn, itemNum)
            
            
        if pathSelector == 3:
            printAllItems(conn)
            
        if pathSelector == 4:
            pass
        if pathSelector == 5:
            pass
    
    if pathSelector == 7:
        custNo = 0
    runInterfaceRec(empId, custNo)

def runInterfaceRec(empIdNo = 0, custIdNumber = 0):
    try:
        runInterface(empIdNo, custIdNumber)
    except Exception:
        traceback.print_exc()
        time.sleep(0.1)
        runInterfaceRec()

runInterfaceRec()