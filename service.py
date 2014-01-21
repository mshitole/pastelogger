# Author: Mahesh Shitole
# Email : maheshshtl@gmail.com

""" service.py contains code to handle windows service

This module responsible for managing the logging and
monitoring the changes in attached devies.
"""

# modules
import win32service
import win32serviceutil
import win32event
import ConfigParser
import os
import time
import sys
import servicemanager


# user define modules
from handle import Process, Drives
from log import Log

# classes and methods

class PySvc(win32serviceutil.ServiceFramework):
    """ class contains the methods for managing the windows service
    """
    _svc_name_ = "PySvc"
    _svc_display_name_ = "PasteLoggerMonitor"
    _svc_description_ = "This service will manage logs for process file handlers"

    def __init__(self, args):
        """ init method
        """
        # set log for service in system log viewer
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, ''))

        win32serviceutil.ServiceFramework.__init__(self,args)
        # create an event to listen for stop requests on
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        # read the config file using config parser
        config = self.read_config()
        name = config.get("Process", "Name")
        path = config.get("Log", "Path") + os.sep + config.get("Log", "Name")
        size = int(config.get("Log", "Size"))
        count = int(config.get("Log", "Count"))
        self.interval = int(config.get("CheckInterval", "Interval"))
        self.log = Log(path, max_bytes=size, backup_count=count)
        self.process = Process()
        self.drives = Drives()

    def read_config(self):
        """ read the configuration file return logfilepath, interval
            and process name
        """
        try:
            config = ConfigParser.ConfigParser()
            config.read(os.path.dirname(__file__) + "\\pastelogger.config")
            return config
        except Exception, err:
            servicemanager.LogInfoMsg("Error while getting pastelogger.config")
            self.SvcStop()

    def SvcDoRun(self):
        """ run when we star the service
        """
        rc = None
        # if the stop event hasn't been fired keep looping
        while rc != win32event.WAIT_OBJECT_0:
            try:
                servicemanager.LogInfoMsg("inside loop")
                # check for device changes in system
                self.drives.watch()
                self.process.log_process_handles()
                time.sleep(self.interval)
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)
            except Exception,err:
                servicemanager.LogInfoMsg("Error while running service : %s " % str(err))

    def SvcStop(self):
        """ tell the SCM we're shutting down
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # fire the stop event
        win32event.SetEvent(self.hWaitStop)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PySvc)