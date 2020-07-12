import pytest
from DB import Ping
from BisnessLogic import BLogic
from datetime import datetime, timedelta, timezone

class GetPings(object):
    def getAllPings(self):
        return [Ping(6928,	'DESKTOP-NIFA-TEST', 91, datetime.now(),	'rgba(61,217,21,0.5)'),
        Ping(6929,	'AAAAAA-H7TU58S', 116, datetime( 2020,7,6, 20,34,3),	'rgba(40,128,80,0.5)'),
        Ping(6930,	'DESKTOP-SOFA-TEST', 142, datetime(2020,7,6 ,20,35,24),	'rgba(11,99,81,0.5)'),
        Ping(6931,	'AAAAAA-H7TU58S', 437, datetime(2020,7,6 , 20,44,40),	'rgba(40,128,80,0.5)'),
        Ping(6932,	'AAAAAA-H7TU58S', 344, datetime(2020,7,6 ,20,54,41),	'rgba(40,128,80,0.5)'),
        Ping(6933,	'DESKTOP-SOFA-TEST', 133, datetime(2020,7,6 ,21,00,21),	'rgba(11,99,81,0.5)')
        ]

sortedData = {}

def setup_function(function):
    da = GetPings()
    bl = BLogic(da)
    global sortedData
    sortedData = bl.createDataTableAndGraph()
     


# def teardown_function(function):
#     global data

#-----------------------------Table------------------------
def test_checkDataTableKey():   
    global sortedData 
    assert list(sortedData.keys())[0] == "TableData"

def test_Table_cottecrNumberOfObjects():
    global sortedData
    assert len(sortedData["TableData"]) == 3

def test_Table_satusDead():
    global sortedData
    for item in sortedData["TableData"]:
        if item['name'] == 'AAAAAA-H7TU58S':
            statusToCheck = item['status']
    assert statusToCheck == 'dead'

def test_Table_satusAlive():
    global sortedData
    for item in sortedData["TableData"]:
        if item['name'] == 'DESKTOP-NIFA-TEST':
            statusToCheck = item['status']
    assert statusToCheck == 'alive'

def test_Table_LatestTime():
    global sortedData
    for item in sortedData["TableData"]:
        if item['name'] == 'AAAAAA-H7TU58S':
            timeToCheck = item['time']
    assert timeToCheck == datetime(2020,7,6 ,20,54,41)


#---------------------Graph---------------------

def test_checkDataGraphKey():   
    global sortedData 
    print(sortedData["GraphData"])
    assert list(sortedData.keys())[1] == "GraphData"

def test_sortDataFromDB_matchPingsToComp():
    global sortedData
    print(sortedData["GraphData"])
    assert len(sortedData["GraphData"]) == 3

def test_Graph_LatestTimeForPing():
    global sortedData
    print(sortedData["GraphData"])
    for item in sortedData["GraphData"]:
        if item['name'] == 'AAAAAA-H7TU58S':
            timeToCheck = item['pingTimeArrray'][-1][1]
    x = datetime(2020,7,6 ,20,54,41, tzinfo=timezone.utc)
    y = x- timeToCheck
    assert timeToCheck == x

