#!/usr/bin/env python


import glob
import sys
import os


if (len(sys.argv) == 1):
    print ("Provide a pattern to match. If you're using wildcards, put them in quotes so the shell doesn't grab it.")
    sys.exit(1)

print ("Searching for files with pattern: " + sys.argv[1])
print ("Adding marker:", sys.argv[2])

listing = glob.glob(sys.argv[1])
pwd = os.getcwd()
for path in listing:
    print path
    dirname = path.split('/')[-1].split('.')[0] + sys.argv[2]
    try:
        os.mkdir(dirname, 0755)
    except OSError, e:
        if e.errno == os.errno.EEXIST:
            print "Directory " + dirname + " already exists, continuing..."
        else:
            raise
    target = os.path.join(pwd,dirname,path.split('/')[-1])
    print "linking from",path,"to",target
    os.symlink(path,target)

    
