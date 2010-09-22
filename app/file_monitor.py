#!/usr/bin/python

from pprint import pprint
import os
import pickle
from hashlib import md5
from time import sleep, time
import sys
import config
import random

import utils
import datetime
import shutil


hostname = utils.get_hostname()

base_folder             = config.hosts[hostname]['base_folder']
monitor_lock            = os.path.join(base_folder,config.monitor['monitor_lock'])
host_lock               = os.path.join(base_folder,hostname + '.lock')
hosts_locks             = [ os.path.join(base_folder,host + '.lock') for host in config.hosts.keys()]
monitor_base_folder     = config.monitor['monitor_base_folder']
music_list_pickle       = os.path.join(base_folder,"music_list.pickle")
transfer_base_folder    = config.transfer['transfer_base_folder']

# Check for the monitor lock
utils.check_lock(monitor_lock,exit=True)

# Check for local host lock
if not utils.check_lock(host_lock):
    utils.aquire_lock(host_lock)

# Check to make sure the other host's lock files are there too
first_time = sys.maxint
first_host = ''
all_in = True

for i in range(0,2): 
    for lock in hosts_locks:
        exists = utils.check_lock(lock)
        if not exists:
            all_in = False
            continue

        (host, timestamp) = exists
        if float(timestamp) < first_time:
            first_host = host
            first_time = float(timestamp)

    if all_in:
        break
    elif i == 0:
        all_in = True
        sleep(60 * 5)

#print "%f" % first_time
print "Winner: %s" % first_host

if first_host == hostname:
    utils.aquire_lock(monitor_lock)
else:
    sys.exit()

music_files = {}
first_pass = True

folders = config.hosts[hostname]['monitor_folders']

# Update the music pickle until all the files have been updated.
while True:
    #print folders
    for folder in folders:
        full_path = os.path.join(base_folder, monitor_base_folder, folder)
        music_files[folder] = []
        #print folder
        for path, dirs, files in os.walk(full_path):
            for f in files:
                #print f
                filename = os.path.abspath(os.path.join(path, f))
                with open(filename,'rb') as fh:
                    hash = md5(fh.read()).hexdigest()
                short_filename = filename[len(base_folder) + len(monitor_base_folder) + 2:]
                music_files[folder].append((short_filename,hash))

        if not music_files[folder]:
            music_files.pop(folder)

    if first_pass:
        first_pass = False
    else:
        f = file(music_list_pickle,'rb') 
        pkl = pickle.load(f)
        f.close()
        if music_files == pkl:
            print "The Same"
            break

    f = file(music_list_pickle,'w') 
    pickle.dump(music_files,f)
    f.close()

    print "sleep 300"
    sleep(300)

# Finished
os.remove(music_list_pickle)

inventory = []

transfer_folder = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%f")
#print transfer_folder
transfer_folder_abs = os.path.join(base_folder, transfer_base_folder,transfer_folder)
#print transfer_folder_abs
os.makedirs(transfer_folder_abs)
#TODO make this a pramameter
uid = int(utils.execute("id -u adam"))
gid = -1
os.chown(transfer_folder_abs,uid,gid)

if music_files:
    print music_files
    delete_folders = set()

    for folder, files in music_files.iteritems():
        for filename,md5 in files:
            full_path = os.path.join(base_folder, monitor_base_folder, filename)
            short_filename = filename[len(folder) +1:]
            new_path = os.path.join(transfer_folder_abs, short_filename)
            directory =  os.path.dirname(short_filename)

            if directory and '.DS_Store' not in short_filename:
                delete_folders.add(os.path.dirname(filename))

            try:
                album_folder = os.path.join(base_folder,transfer_base_folder,transfer_folder,directory)
                os.makedirs(album_folder)
            except:
                pass

            shutil.move(full_path,new_path)
            
            inventory.append((short_filename,md5,folder))

    for folder in delete_folders:
        for i in range(folder.count('/'),0,-1):
            sub_folder = '/'.join(folder.split('/')[:i+1])
            try:
                shutil.rmtree(os.path.join(base_folder, monitor_base_folder, sub_folder))
            except OSError:
                pass
    try:
        #pprint(inventory)
        f = file(os.path.join(transfer_folder_abs,'inventory.pickle'),'w') 
        pickle.dump(inventory,f)
        f.close()
    except:
        pass

for host_lock in hosts_locks:
    try:
        os.remove(host_lock)
    except:
        pass

monitor_completed = os.path.join(base_folder, 'monitor.completed')
aquire_lock(monitor_completed)

os.remove(monitor_lock)
