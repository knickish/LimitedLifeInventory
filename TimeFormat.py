'''
Created on Sep 16, 2018

@author: Sauruk
'''
import time

def currTime():
    return (int(time.time()))/100

def timeDiff(epochTime):
    return (currTime()-epochTime)