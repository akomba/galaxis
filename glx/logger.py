import logging
from logging.handlers import TimedRotatingFileHandler
import glx.helper as helper
import os

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=Singleton):
    def __init__(self,community_name):
        # DEBUG INFO WARNING ERROR CRITICAL
        # get community root folder
        cc = helper.load_community_config(community_name)
        logfilename = os.path.join(cc["log_folder"],community_name+".log")
        #handler = TimedRotatingFileHandler(logfilename, when="midnight", backupCount=30)
        handler = TimedRotatingFileHandler(logfilename, when="midnight", interval=1)
        handler.suffix = "%Y%m%d"
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
