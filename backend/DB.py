import mysql.connector
from datetime import datetime, timedelta
import config as conf

class dataAccess(object):
    def __init__(self):
         self.mydb = mysql.connector.connect(
            host=conf.mysql["host"],
            user=conf.mysql["user"],
            password=conf.mysql["password"],
            database=conf.mysql["database"]
          )

    def addCompToDB(self, compName):
          mycursor = self.mydb.cursor()
          sql = "INSERT INTO ping_management.comps (compName)  VALUES (%s); "
          val = (compName,) 
          mycursor.execute(sql, val)
          self.mydb.commit()
          print(mycursor.rowcount, "record inserted.")

    def addNewPings(self, data):
        mycursor = self.mydb.cursor()
        compName = data['test_url']#!??
        ping = data['ping']#!??
        timeStem = datetime.now()
        if not ping:
            ping = 0
        args = [compName, ping, timeStem]
        result_args = mycursor.callproc('ping_management.add', args)
        

    # def addPingToDB(self,compName, ping, timeStem):
    #     mycursor = self.mydb.cursor()
    #     sql = "INSERT INTO ping_management.pings (compName, ping, timeOfResponce)  VALUES (%s, %s, %s); "
    #     val = (compName, ping, timeStem)
    #     mycursor.execute(sql, val)
    #     self.mydb.commit()
    #     print(mycursor.rowcount, "record inserted.")
 
    def deleteComp(self, compName):       
        mycursor = self.mydb.cursor()
        args = [compName]
        print('comp name '+compName)
        result_args = mycursor.callproc('ping_management.delete', args)
        for result in mycursor.stored_results():
          print (result.fetchall())
        print(result_args)
        print(mycursor.rowcount)
        return mycursor.rowcount 

    # def getAllComps(self):        
    #     mycursor = self.mydb.cursor()
    #     mycursor.execute("SELECT compName from ping_management.comps ORDER BY id")
    #     distComps = mycursor.fetchall()
    #     return map(lambda item:''.join(item), distComps) 

    def getAllPings(self):        
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM ping_management.pings")
        allPings = mycursor.fetchall() 
        return allPings

    # def getLastPing(self, compName):
    #     mycursor = self.mydb.cursor()
    #     mycursor.execute("SELECT * from ping_management.pings where compName =\'"+compName+"\' ORDER BY timeOfResponce DESC LIMIT 1")
    #     return mycursor.fetchone()

    # def getTableData(self):
    #     result = []
    #     distComps = self.getAllComps()
    #     # print(distComps)
    #     for name in distComps:
    #        result.append(self.getLastPing(name))
    #     return result
        
 

    # def infoByComp(self, compName):
    #       mycursor = self.mydb.cursor()
    #       mycursor.execute("SELECT compName,ping, timeOfResponce from ping_management.pings where compName =\'"+compName+"\' ORDER BY timeOfResponce ASC") 
    #       return mycursor.fetchall()
    

    

    
# s= dataAccess()
# s.getAllPings()