import mysql.connector
from datetime import datetime, timedelta, timezone
import config as conf
import logging
import random
import math

logger = logging.getLogger(__name__)

class dataAccess(object):
    def __init__(self, mode, config):
      self.mode = mode
      self.config =config
      self.mydb =  mysql.connector.connect(
          host=self.config.get_host(),
          user=self.config.get_user(),
          password=self.config.get_password(),
          database=self.config.get_database()
          )
       

    def addCompToDB(self, compName):
      try:
          logger.info('In FUNCTION %s data before insert: %s', 'addCompToDB', compName)
          mycursor = self.mydb.cursor()
          sql = "INSERT INTO  comps (compName)  VALUES (%s); "
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
          compName = data['hostname']#!??
          ping = data['ping']#!??
          timeStem = datetime.now(timezone.utc)
          color = "rgba(" + str(math.floor(random.random() * 255)) + "," + str(math.floor(random.random() * 255)) + "," + str(math.floor(random.random() * 255)) + ",0.5)"
          args = [compName, ping, timeStem, color]
          logger.info('In FUNCTION %s data before insert: %s\n', 'addNewPings', args)
          result_args = mycursor.callproc('addPing', args)
          logger.info('In FUNCTION %s data before insert: %s\n', 'addNewPings', result_args)
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'addNewPings', e)  
          raise

    def deleteComp(self, compName):
      try:  
        mycursor = self.mydb.cursor()
        args = [compName, 0]
        logger.info('In FUNCTION %s data before delete: %s\n', 'deleteComp', args)
        result_args = mycursor.callproc('deletePingsToComp', args)
        logging.info('In FUNCTION %s data after insert: %s\n', 'deleteComp', result_args)
        return result_args[1] 
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'deleteComp', e)  
          raise

    def deleteAll(self):
      try:  
        if self.mode == 'test':
          mycursor = self.mydb.cursor()
          args = [0]
          logger.info('In FUNCTION %s data before delete: %s\n', 'deleteComp', args)
          result_args = mycursor.callproc('deleteAll', args)
          logging.info('In FUNCTION %s data after insert: %s\n', 'deleteComp', result_args)
          return result_args[0] 
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'deleteComp', e)  
          raise

    def getAllPings(self):
      try:      
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT pings.id, pings.compName, pings.ping, pings.timeOfResponce, comps.lineColor FROM  pings INNER JOIN  comps ON  pings.compName =  comps.compName")
        allPingsTuples = mycursor.fetchall()
        allPings = list(map(lambda ping: Ping(ping[0], ping[1], ping[2], ping[3].replace(tzinfo= timezone.utc), ping[4]),allPingsTuples) )
        return allPings
      except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', 'getAllPings', e)  
          raise

class Ping(object):
  def __init__(self, id, compName, pingValue, time, color):
    self.id = id
    self.compName = compName
    self.pingValue = pingValue
    self.time = time
    self.color = color

  def __str__(self):
    return "id -- {id}, compName -- {comp}, pingValue -- {value}".format(id=self.id, comp=self.compName, value = self.pingValue) 
    



# s= dataAccess()
# s.deleteComp('www.calorizator.ru')