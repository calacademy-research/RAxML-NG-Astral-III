#!/usr/bin/env python


import subprocess
import os
import sys
import math
import glob
from os import listdir
from os.path import isfile, join
import multiprocessing

# Example that spawns one process for each file in a directory.
cur_process_count = 0
target_process_count = 2
run_array = "/home/bsimison/raxml-ng/bin/raxml-ng --msa FILENAME --model GTR+G --threads 2".split(' ');



def get_target_process_count(target_threads_per_process):
    # target_threads_per_process = 2
    cores = multiprocessing.cpu_count()
    print "Total cores:", cores
    cur_load = int(math.ceil(os.getloadavg()[0]))
    print "Current load:", cur_load
    available_cores = cores - cur_load
    print "Available cores:", available_cores
    num_processes = int(round(available_cores / target_threads_per_process))
    print "number of processes we can run:", num_processes
    return num_processes


def get_files_in_argv():
    if (len(sys.argv) == 1):
        print (
            "Provide a pattern to match. If you're using wildcards, put them in quotes so the shell doesn't grab it.")
        sys.exit(1)

    print ("Searching for files with pattern: " + sys.argv[1])

    listing = glob.glob(sys.argv[1])
    return listing


def launch_process(file_with_path):
    argArray = run_array
    argArray[2] = file_with_path.split('/')[-1]
    # argArray.append(run_string)
    # argArray.append(file_with_path.split('/')[-1])
    target_dir = os.path.dirname(file_with_path)
    print "Running: ", argArray
    print "in dir", target_dir

    pid = subprocess.Popen(argArray,
                           cwd=target_dir,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    return pid

def launch_processes(process_file_list):
    print "Batch contains:", process_file_list
    pids = []
    for cur_file in process_file_list:
        pids.append(launch_processes(cur_file))

    for pid in pids:
        pid.wait()

def pop_n(n, list):
    ret_val = []
    while n > 0 and len(list) > 0:
        ret_val.append(list.pop())
        n -= 1
    return ret_val

def do_runs(file_list):
    print "Processing", len(file_list), "files...."
    while len(file_list) > 0:
        launch_processes(pop_n(target_process_count, file_list))

files = get_files_in_argv()
do_runs(files)
