from collections import namedtuple
from DB import *
import config as conf
import logging
import pytz
import json
from datetime import timezone, datetime

logger = logging.getLogger(__name__)


class BLogic(object):
    def __init__(self, dataAccess=''):
        self.dataAccess = dataAccess
    

    def createDataTableAndGraph(self):
        try:  
            data  = self.dataAccess.getAllPings()
            tableData = self.getTableData(data)
            graphData = self.getGraphData(data)
            return {"TableData": tableData,  "GraphData": graphData}
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s',
                         'createDataTableAndGraph', e)
            raise

    def isAlive(self, time):
        try:
            
            isAlive = timedelta(seconds=4*conf.delay_time).total_seconds() >= (datetime.now(timezone.utc) - time).total_seconds()
            logger.info('In FUNCTION %s data before \'return\': %s\n', 'isAlive', isAlive)
            return isAlive
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'isAlive', e)
            raise

    def getTableData(self, data):
        try:
            dictComps = self.sortDataFromDB(data)
          
            def getCompInfo(compNamePings):
                compName, pings = compNamePings
                pings.sort(key=lambda ping: ping.time)
                lastPing = pings[-1]
                return CompTableInfo(
                    lastPing.id,
                    lastPing.compName,
                    lastPing.pingValue,
                    lastPing.time ,
                    'alive' if self.isAlive(lastPing.time) else 'dead'                  
                ).dictionary() 
            return list(map(getCompInfo, dictComps.items()))
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s',
                         'getTableData', e)
            raise

    def getGraphData(self, data):
        try:
            dictComps = self.sortDataFromDB(data)

            def getCompGraphData(compNamePings):
                compName, pings = compNamePings
                pings.sort(key=lambda ping: ping.time)
                color = dictComps[compName][0].color
                pingTimeArray = list(map(lambda item : (item.pingValue, item.time),pings))
                return CompGraphInfo(
                    compName,
                    color,
                    pingTimeArray
                ).dictionary()
            return list(map(getCompGraphData, dictComps.items()))

        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s',
                         'getGraphData', e)
            raise

    def sortDataFromDB(self, data):
        try:
            comps = set(map(lambda ping:  ping.compName, data))
            return  {comp: list(filter(lambda ping: ping.compName  == comp, data)) for comp in comps}
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s',
                         'sortDataFromDB', e)
            raise
class CompTableInfo(object):
    def __init__(self, id, name, ping, time, status ):
         self.id = id
         self.name = name
         self.ping = ping
         self.time= time
         self.status = status

    def dictionary(self):
        return {'id':str(self.id),
                'name': self.name,
                'ping':str(self.ping),
                'time': self.time,
                'status':self.status
                }
    
class CompGraphInfo(object):
    def __init__(self, name, color, pingTimeArray):
         self.name = name
         self.color = color
         self.pingTimeArray= pingTimeArray

    def dictionary(self):
        return { 'name': self.name,
                'color':str(self.color),
                "pingTimeArrray": self.pingTimeArray
                }