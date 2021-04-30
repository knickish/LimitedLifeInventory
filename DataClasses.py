'''
Created on Sep 15, 2018

@author: Sauruk
'''
from Database import findItemName
import time
from TimeFormat import currTime

__all__ = ["itemCounter", "item", "label"]

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
    lifetime = 12345
    
    
    
    def __init__(self, name, itemNumber, lifetime):
        self.itemName = name
        self.itemNumber = itemNumber
        self.lifetime = lifetime
        
        
class label:
    def __init__(self, uId, itemNumber, initTime, lifeRemaining, creatorId, note = ''):
        self.uid = uId
        self.itemNumber = itemNumber
        self.initTime = initTime
        self.creatorId = creatorId
        self.lifeTime = lifeRemaining
        self.itemNotes[0] = note 
    
    def printLabel(self, db):
        name = findItemName(db, self.itemNumber)
        lifeRemaining = self.getLifeRemaining()
        lifeMonths = lifeRemaining / 720
        lifeRemaining = lifeRemaining % 720
        lifeDays = lifeRemaining / 24
        lifeRemaining = lifeRemaining % 24
        print( "<%s : %s Expires in %s Months, %s Days, and %s Hours>", (self.uid, name, lifeMonths, lifeDays, lifeRemaining ))
    
    def addNote(self, note):
        self.itemNotes[len(self.itemNotes)] = note


    def getLifeRemaining (self):
        lifeRemaining = (self.initTime + self.lifetime*60 -currTime())
        return lifeRemaining