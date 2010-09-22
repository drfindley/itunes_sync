import os
import sys
from time import sleep, time

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

def check_lock(lock_file,exit=False):
    for i in range(0,2):
        if os.path.exists(lock_file):
            #print "Lock exists: %s" % lock_file
            if exit:
                sys.exit(0)
            else:
                with open(lock_file,'r') as lock:
                    l = lock.read()
                    #(host, timestamp) = l.split()
                    #print l.split()
                    #print host, timestamp
                    return l.split()
        return None
        #sleep(5)

def aquire_lock(lock_file):
    if os.path.exists(lock_file):
        print "Lock already aquired"
        sys.exit(0)

    with open(lock_file, 'w') as lock:
        lock.write("%s %f" % (get_hostname(), time()))

def remove_lock(lock_file):
    if os.path.exists(lock_file):
        print "Lock already aquired"
        sys.exit(0)
    open(lock_file, 'w').close()

def is_root():
    whoami = execute('whoami')
    if whoami == 'root':
        return True

    return False

def load_agent(agent):
    print "sudo launchctl load %s" % agent
    execute("launchctl load %s" % agent)

def unload_agent(agent):
    print "sudo launchctl unload %s" % agent
    execute("launchctl unload %s" % agent)
