import mysql.connector
from datetime import datetime, timedelta
import config as conf
import logging

logger = logging.getLogger(__name__)

class dataAccess(object):
    def __init__(self):
         self.mydb = mysql.connector.connect(
            host=conf.mysql["host"],
            user=conf.mysql["user"],
            password=conf.mysql["password"],
            database=conf.mysql["database"]
          )

    def addCompToDB(self, compName):
      try:
          logger.info('In FUNCTION %s data before insert: %s', 'addCompToDB', compName)
          mycursor = self.mydb.cursor()
          sql = "INSERT INTO ping_management.comps (compName)  VALUES (%s); "
          val = (compName,) 
          mycursor.execute(sql, val)
          self.mydb.commit()
          logger.info('In FUNCTION %s number of record inserted: %s', 'addCompToDB', mycursor.rowcount)
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'addCompToDB', e)  
          raise

    def addNewPings(self, data):
      try:
          mycursor = self.mydb.cursor()
          compName = data['test_url']#!??
          ping = data['ping']#!??
          timeStem = datetime.now()
          if not ping:
              ping = 0
          args = [compName, ping, timeStem]
          logger.info('In FUNCTION %s data before insert: %s\n', 'addNewPings', args)
          result_args = mycursor.callproc('ping_management.add', args)
          logger.info('In FUNCTION %s data before insert: %s\n', 'addNewPings', result_args)
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'addNewPings', e)  
          raise

    def deleteComp(self, compName):
      try:  
        mycursor = self.mydb.cursor()
        args = [compName, 0]
        logger.info('In FUNCTION %s data before delete: %s\n', 'deleteComp', args)
        result_args = mycursor.callproc('ping_management.delete', args)
        logging.info('In FUNCTION %s data after insert: %s\n', 'deleteComp', result_args)
        return result_args[1] 
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'deleteComp', e)  
          raise

    def getAllPings(self):
      try:      
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM ping_management.pings")
        allPings = mycursor.fetchall() 
        return allPings
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'getAllPings', e)  
          raise

 
    

    



# s= dataAccess()
# s.deleteComp('www.calorizator.ru')