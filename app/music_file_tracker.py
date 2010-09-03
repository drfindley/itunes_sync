#!/usr/bin/python

from pprint import pprint
import os
import pickle
from hashlib import md5
from time import sleep
import sys
import config
import random

from utils import get_hostname, combine_dicts, aquire_lock

hostname = get_hostname()

# FILE
music_dir = config.hosts[hostname]['music_folder']
music_list_pickle = os.path.join(music_dir,"music_list.pickle")
history_pickle = os.path.join(music_dir,"history.pickle")
lock_file = os.path.join(music_dir,"file_tracker.lock")
computers_pickle = os.path.join(music_dir,"computers.pickle")
folders = ['Emusic','iTunes','AmazonMP3','other']

def history_md5s():
    if os.path.exists(history_pickle):
        f = open(history_pickle,'rb')
        history = pickle.load(f)
        f.close()

        md5s = [file_tuple[1] for sources in history.values() for file_tuple in sources]
        return md5s
    return []

sleep(config.hosts[hostname]['start_time'])

aquire_lock(lock_file)

music_files = {}
first_pass = True
md5s = history_md5s()

# Update the music pickle until all the files have been updated.
while True:
    print folders
    for folder in folders:
        full_path = os.path.join(music_dir, folder)
        music_files[folder] = []
        print folder
        for path, dirs, files in os.walk(full_path):
            for f in files:
                print f
                filename = os.path.abspath(os.path.join(path, f))
                fh = open(filename,'rb')
                hash = md5(fh.read()).hexdigest()
                if hash in md5s:
                    continue
                short_filename = filename[len(music_dir) + 1:]
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

    #pprint(music_files)
    f = file(music_list_pickle,'w') 
    pickle.dump(music_files,f)
    f.close()

    print "sleep 240"
    sleep(240)

# Finished
os.remove(music_list_pickle)

history = {}
if os.path.exists(history_pickle):
    f = open(history_pickle,'rb')
    history = pickle.load(f)
    f.close()

history = combine_dicts(history,music_files)
#pprint(history)

f = open(history_pickle,'w')
pickle.dump(history,f)
f.close()

computers = {}
if os.path.exists(computers_pickle):
    f = open(computers_pickle,'r')
    computers = pickle.load(f)
    f.close()

for key in config.hosts.keys():
    computers[key] = combine_dicts(music_files,computers.get(key,{}))

#pprint(computers)

f = open(computers_pickle,'w')
pickle.dump(computers,f)
f.close()

sleep(60)

os.remove(lock_file)
