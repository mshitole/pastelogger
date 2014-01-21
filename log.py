# Author: Mahesh Shitole
# Email : maheshshtl@gmail.com

""" log.py contains wrapper around the logger

This module handles the logging as well as log rotating
Simple abstract around logger.

Creating a singletone class neccessary here.
"""

# modules
import logging
import logging.handlers

# classes and methods

class Singleton(type):
    """ singleton class meta type
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                    **kwargs)
        return cls._instances[cls]

class Log(object):
    """ log class definition
    """
    __metaclass__ = Singleton
    def __init__(self, log_file_name, mode='a', max_bytes=10, backup_count=2):
        """ Set up a specific logger with our desired output level
        """
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.my_logger = logging.getLogger('MyLogger')
        self.my_logger.setLevel(logging.DEBUG)

        self.log_file_name = log_file_name
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
              log_file_name, mode, max_bytes, backup_count)
        handler.setFormatter(formatter)
        self.my_logger.addHandler(handler)

    def debug(self, msg):
        """ debug level
        """
        self.my_logger.debug(msg)

    def info(self, msg):
        """ info level
        """
        self.my_logger.info(msg)

    def error(self, msg):
        """ error level
        """
        self.my_logger.error(msg)
