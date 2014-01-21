pastelogger
===========

pastelogger is a script to keep all logs of files which are open, copy and move by user

pull requests are welcome !!!

License: OPEN to all

Features:
  > Simple to run.
  
  > Windows service.
  
  > Logs all the file open by copy paste operations in windows.
  
  > Keep logs for all the usb devices attach to the system.
  
Dependencies:
  > psutil
  
How to run ?
  > first configure pastelogger.config file 
  
  > Meaning of each parameter is explain bellow:
  
    [Process]
    Name = explorer.exe (name of the process which you want to monitor)

    [Log]
    Path = C:\Users\mahesh (path where all the logs get stored)
    Name = pastelogger.log  (log file name)
    Size = 20000 (total size of the log file in BYTES)
    Count = 2 (no of log file maintain)

    [CheckInterval]
    Interval = 3000 (no of milliseconds we have to monitor the process)

    > now configure this file according to your requirement
    
    > install this serive using python service install
    
    > start the service
    
    > now do any file operations and observe log file
      
    > expected that all the file handles which are using by particular process gets added in log file.

Todo List:
  > Need to add installer.
  
  > Have to support linux OS.
  
  > Need to be more robust for performance point of view