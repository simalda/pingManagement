import mysql.connector
from datetime import datetime, timedelta
 




class SQL(object):
    def __init__(self):
         self.delay_time =  600
        #  timedelta(minutes=5)
         self.mydb = mysql.connector.connect(
            host="localhost",
            user="roma",
            password="Aa123456",
            database="ping_management"
          )

    def addCompToDB(self, compName):
          mycursor = self.mydb.cursor()
          sql = "INSERT INTO ping_management.comps (compName)  VALUES (%s); "
          print(sql)
          val = (compName,)#!!!
          print(val)
          mycursor.execute(sql, val)
          self.mydb.commit()
          print(mycursor.rowcount, "record inserted.")

    def addNewPings(self, data):
        compName = data['test_url']
        ping = data['ping']
        timeStem = datetime.now()
        distComps = self.getAllComps()
        if compName not in distComps:
          self.addCompToDB(compName)
        self.addPingToDB(compName, ping, timeStem)

    def addPingToDB(self,compName, ping, timeStem):
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO ping_management.pings (compName, ping, timeOfResponce)  VALUES (%s, %s, %s); "
        val = (compName, ping, timeStem)
        mycursor.execute(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    def deleteComp(self, compName):        #letaken
        mycursor = self.mydb.cursor()
        sql = "DELETE FROM pings WHERE compName = \'" + compName + "\'"
        mycursor.execute(sql)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")
        mycursor2 = self.mydb.cursor()
        sql2 = "DELETE FROM comps WHERE compName = \'" + compName + "\'"
        mycursor2.execute(sql2)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) deleted")


    def getAllComps(self):        
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT compName from ping_management.comps")
        distComps = mycursor.fetchall()#MITYA
        # print(distComps)
        return map(lambda item:''.join(item), distComps) 
        

    
 
    def getCharData(self):
        result = []        
        distComps = self.getAllComps()
        # print(distComps)
        for name in distComps:
              pingTimeArray = []
              compInfo = self.infoByComp(name)
              for item in compInfo:
                pingTimeArray.append((item[1], item[2]))                 
              result.append(
                  {
                    "compName" :item[0],
                    "pingTimeArrray":pingTimeArray
                    # "timeStepsArray":timeStepsArray
                  }
                )    
        # print(result)       
        return result

    def getLastPing(self, compName):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * from ping_management.pings where compName =\'"+compName+"\' ORDER BY timeOfResponce DESC LIMIT 1")
        return mycursor.fetchone()
        

    def getTableData(self):
        result = []
        distComps = self.getAllComps()
        # print(distComps)
        for name in distComps:
           result.append(self.getLastPing(name))
        return result
        
    def getPings(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM pings")
        myresult = mycursor.fetchall()
        # for x in myresult:
        #   print(x)
        return myresult   


    def infoByComp(self, compName):
          mycursor = self.mydb.cursor()
          mycursor.execute("SELECT compName,ping, timeOfResponce from ping_management.pings where compName =\'"+compName+"\' ORDER BY timeOfResponce ASC") 
          return mycursor.fetchall()
    
    def isAlive(self, compName, time):
        print('from is ALIVE')
        print(str(timedelta(seconds=4*self.delay_time).total_seconds()))
        print(str((datetime.now() - time).total_seconds()))
        print( timedelta(seconds=4*self.delay_time).total_seconds() >= (datetime.now() - time).total_seconds())
        return  timedelta(seconds=4*self.delay_time).total_seconds() >= (datetime.now() - time).total_seconds()
    

    
# s= SQL()
# s.addCompToDB('hhd' )