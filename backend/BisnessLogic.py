from DB import *
import config as conf

class BLogic(object):
    def createDataTableAndGraph(self):
        s = dataAccess()
        data = s.getAllPings()
        tableData = self.getTableData(data)
        graphData = self.getGraphData(data)
        return {"TableData":tableData,  "GraphData":graphData}

    def isAlive(self, time):
        return  timedelta(seconds=4*conf.delay_time).total_seconds() >= (datetime.now() - time).total_seconds()

    def  getTableData(self, data):
        TableDataInfo = []
        distComps = self.sortDataFromDB(data)
        for compName in distComps.keys():
              pingTimeArray = []
              distComps[compName].sort(key=lambda x:x[3])              
              status =  'alive' if self.isAlive(distComps[compName][-1][3]) else 'dead'
              singlePing = {
                "id": distComps[compName][-1][0],
                "name": distComps[compName][-1][1],
                "ping": distComps[compName][-1][2],
                "time": distComps[compName][-1][3],
                "status":  status
            }
              TableDataInfo.append(singlePing)
        return TableDataInfo

    def getGraphData(self, data):
        result = []
        distComps = self.sortDataFromDB(data)
        for compName in distComps.keys():
              pingTimeArray = []
              distComps[compName].sort(key=lambda x:x[3])
              for item in distComps[compName]:
                pingTimeArray.append((item[2], item[3]))                 
              result.append(
                  {
                    "compName" :compName,
                    "pingTimeArrray":pingTimeArray
                  }
                )    
        return result

    def sortDataFromDB(self, data):
        dataDict = {}
        for ping in data:
            if ping[1] not in dataDict.keys():
                dataDict[ping[1]] = [ping]
            else:
                dataDict[ping[1]].append(ping)
        return dataDict