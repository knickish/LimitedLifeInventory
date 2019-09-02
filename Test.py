'''
Created on Sep 22, 2018

@author: Sauruk
'''
from __init__ import getLoginInfo, getItemTypes, getNumberXNameMap, getCats, getAllItems, getAllByCat
from Database import *
from TimeFormat import currTime
from flask import jsonify
import json



getLoginInfo()


print(getAllByCat(361047))