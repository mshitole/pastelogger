# Author: Mahesh Shitole
# Email : maheshshtl@gmail.com

""" handle.py contains wrapper around the logger

This module handles the usb detection for the usb
"""

# modules
import psutil
import win32file
import win32api
import string
from ctypes import windll

# user define modules 
from log import Log

# constants
ESCAPE_DIRS = [
        "C:\\Windows",
    ]

class Drives(object):
    """ class to get the drive list.
    """
    def __init__(self):
        """ init function will call get drives function and make 
        list of all the device that are available and add it to 
        Drives.drives which is static variable further require to
        computing.
        """
        self.log =  Log()
        Drives.drives = self.get_drives()

    def get_drives(self):
        """ function to drive list
        """
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        return drives
    
    def get_drive_stats(self, drive):
        """ function to get the drive information
        returns total_space, free_space, used space
        """
        gb = float(1024 * 1024 * 1024)
        sec_per_cl, byte_per_cl, free_cl, tot_cl = \
            win32file.GetDiskFreeSpace(drive + ":\\")
        total_space = tot_cl * sec_per_cl * byte_per_cl
        free_space = free_cl * sec_per_cl * byte_per_cl
        return total_space / gb, free_space / gb, (total_space - free_space) / gb

    def watch(self):
        """ watch function will ping system continuouly for hardware change
        if it found that there is any usb device attched then 
        this will log that usb information
        """
        tmpdrives = self.get_drives()
        if len(Drives.drives) !=  len(tmpdrives):
            self.log.debug("Detected hardware changes")

        for dri in Drives.drives:
            if dri not in tmpdrives:
                self.log.debug("Drive removed: %s\\" % dri)

        for dri in tmpdrives:
            if dri not in Drives.drives:
                self.log.debug("New drive attached to system: %s\\" % dri)
                to_sp, free_sp, use_sp = self.get_drive_stats(dri)
                self.log.debug("Disk Space Information:")
                self.log.debug("Total Space: %s Bytes" % (to_sp))
                self.log.debug("Free Space : %s Bytes" % (free_sp))
                self.log.debug("Used Space : %s Bytes" % (use_sp))

        Drives.drives = tmpdrives


class Process(object):
    """ class process use to deal with process
    use to get handles for the process
    """
    def __init__(self, name='explorer.exe'):
        """ take by default explorer.exe argument it can be process
        process name
        """
        self.log = Log()
        self.name = name
        self.pid = self.get_process_id()

    def get_process_id(self):
        """ function returns the process id of the process
        """
        for proc in psutil.process_iter():
            if proc.name == self.name:
                return proc.pid

    def log_process_handles(self):
        """ function to get the list of the file handles open by process
        """
        res = []
        proc = psutil.Process(self.pid) # or PID of process
        for fh in proc.get_open_files():
            if self.check_escape_dir(fh.path):
                continue
            if fh.path not in res:
                res.append(fh.path)
        if res:
            self.log.debug("File handle path open by process:")
            for path in res:
                self.log.debug(str(path))
        return res

    def check_escape_dir(self, path):
        """ filter the system files handles from process
        accept path as input and check in ESCAPES_DIRS if present then 
        return True else False
        """
        for edir in ESCAPE_DIRS:
            if edir in path:
                return True
        return False