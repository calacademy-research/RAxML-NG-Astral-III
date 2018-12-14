

import subprocess
import os
import sys
from os import listdir
from os.path import isfile, join

# Example that spawns one process for each file in a directory.

def runMe(argArray):
    print("Running: " + argArray[0])
    p = subprocess.Popen(argArray,
                         cwd="./",
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

def spawnDaemon(func):
    print("1")
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # parent process, return and keep running
            return
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    os.setsid()

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # do stuff
    print("Runnnnnn")
    func()

    # all done
    os._exit(os.EX_OK)



allFiles = listdir("./")
fileCount=1
everyN = 5
executeString = ""
for file in allFiles:

    if(isfile(file)):

        # if executeString is == 0 then executeString + file else
        if executeString == "":
            executeString += file
        else:
            executeString = executeString + " " + file
        if fileCount % everyN == 0:

            spawnDaemon(runMe(['say',executeString]))
            # call (["nohup","say", executeString, "&"])
            executeString = ""

        fileCount += 1




# Iterate over everything in a directory
# Create an empty string called "executeString"
# If the thing in question is actually a string, then:
#   append it to the end of executeString
#   If our counter is evenly divisible by everyN (5, in this case) then
#      print a pretty header
#      Clear out execute string so we can start over.
#   Increment the counter
