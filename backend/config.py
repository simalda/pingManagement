import json
import logging


logger = logging.getLogger(__name__)

class Config:
    def __init__(self, file):
        print(file)        
        f = None
        try:  
            f = open(file, "r")
            logger.info('In FUNCTION %s after opening config file: %s\n', '__init__', f)
            self.config = json.load(f)
            logging.info('In FUNCTION %s data from config file: %s\n', '__init__', self.config)
            print(self.config)
           
        except Exception as e:
          logger.error('In FUNCTION %s exception raised: %s', '__init__', e)  
          raise
        finally:
            if f != None:
                f.close()
    
    # getter method 
    def get_host(self): 
        return self.config['mysql']['host']
    def get_user(self): 
        return self.config['mysql']['user']
    def get_password(self): 
        return self.config['mysql']['password']
    def get_database(self): 
        return self.config['mysql']['database']

    def get_delay_time(self): 
        return self.config['delay_time']

 
         




# c = Config("C:\\Users\\simal\\projects_git\\ping_management\\backend\\config_test.txt")
  