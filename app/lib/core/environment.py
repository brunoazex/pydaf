import yaml
import os, inspect

class Environment(object):
    def __init__(self, config_path): 
        try:            
            self.mode = os.getenv('APP_MODE', None) or 'DEV' 
            with open(r'%s/config/%s.yml' % (config_path, self.mode.lower())) as file:
                dataMap = yaml.safe_load(file)
                self.__merge_app_settings(dataMap)
                self.database = self.__load_db_settings(dataMap)
                self.processors = self.__Item(dataMap['processors'])
        except Exception as error:
            print('Cannot initialize configuration: %s' % error)
    
    def __merge_app_settings(self, dataMap):
        self.__dict__.update(**dataMap['app'])
        
    def __load_db_settings(self, dataMap): 
        # Database environment variables takes precedence over config file variables
        return self.__Item({
            'host': os.getenv('DB_HOST', None) or dataMap['database']['host'],
            'database': os.getenv('DB_NAME', None) or dataMap['database']['database'],
            'user': os.getenv('DB_USER', None) or dataMap['database']['user'],
            'password': os.getenv('DB_PASS', None) or dataMap['database']['password']
        })
        
    class __Item(object):
        def __init__(self, entries):
            self.__dict__.update(**entries)