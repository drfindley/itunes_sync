import os
import sys

def execute(cmd):
    import subprocess
    
    proc = subprocess.Popen(cmd,shell=True,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = proc.communicate()

    stdout = output[0].strip()
    stderr = output[1].strip()

    return stdout

def get_hostname():
   return execute("scutil --get ComputerName")

def combine_dicts(one,two):
    keys = set(one.keys() + two.keys())
    out = {}
    for key in keys:
        out[key] = list(set(one.get(key,[]) + two.get(key,[])))
    return out

def aquire_lock(lock_file):
    if os.path.exists(lock_file):
        print "Lock already aquired"
        sys.exit(0)
    open(lock_file, 'w').close()
