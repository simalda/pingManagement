from DB import *
import config as conf
import logging
import pytz
logger = logging.getLogger(__name__)

class BLogic(object):
    def __init__(self):
        self.lastPing = -1
        self.id = 0
        self.compName = 1
        self.pingValue = 2
        self.time = 3
         
        
    def createDataTableAndGraph(self):
        try:
            s = dataAccess()
            data = s.getAllPings()
            tableData = self.getTableData(data)
            graphData = self.getGraphData(data)
            return {"TableData":tableData,  "GraphData":graphData}
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'createDataTableAndGraph', e)  
            raise

    def isAlive(self, time):
        try:
            logger.info('In FUNCTION %s data before \'return\': %s\n', 'isAlive' , timedelta(seconds=4*conf.delay_time).total_seconds() >= (datetime.now() - time).total_seconds())
            return  timedelta(seconds=4*conf.delay_time).total_seconds() >= (datetime.now() - time).total_seconds()
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'isAlive', e)  
            raise

    def  getTableData(self, data):
        try:
            TableDataInfo = []              
            distComps = self.sortDataFromDB(data)
            for compName in distComps.keys():
                distComps[compName].sort(key=lambda x:x[self.time])              
                status =  'alive' if self.isAlive(distComps[compName][self.lastPing][self.time]) else 'dead'
                singlePing = {
                    "id": distComps[compName][self.lastPing][self.id],
                    "name": distComps[compName][self.lastPing][self.compName],
                    "ping": distComps[compName][self.lastPing][self.pingValue],
                    "time": distComps[compName][self.lastPing][self.time],
                    "status":  status

                }
                print(distComps[compName][self.lastPing][self.time])
                print(type(distComps[compName][self.lastPing][self.time]))
                TableDataInfo.append(singlePing)
            logger.info('In FUNCTION %s data before \'return\': %.3000s\n', 'getTableData', TableDataInfo)
            return TableDataInfo
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'getTableData', e)  
            raise

    def getGraphData(self, data):
        try:
            result = []
            distComps = self.sortDataFromDB(data)
            for compName in distComps.keys():
                pingTimeArray = []
                distComps[compName].sort(key=lambda x:x[self.time])
                for item in distComps[compName]:
                    pingTimeArray.append((item[self.pingValue], item[self.time].astimezone(pytz.utc)))                 
                result.append(
                    {
                        "compName" :compName,
                        "pingTimeArrray":pingTimeArray
                    }
                    )    
            logger.info('In FUNCTION %s data before \'return\': %.3000s\n', 'getGraphData', result)
            return result
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'getGraphData', e)  
            raise

    def sortDataFromDB(self, data):
        try:
            dataDict = {}
            for ping in data:
                if ping[self.compName] not in dataDict.keys():
                    dataDict[ping[self.compName]] = [ping]
                else:
                    dataDict[ping[self.compName]].append(ping)
            logger.info('In FUNCTION %s data before \'return\': %.3000s\n', 'sortDataFromDB', dataDict)
            return dataDict
        except Exception as e:
            logger.error('In FUNCTION %s exception raised: %s', 'sortDataFromDB', e)  
            raise