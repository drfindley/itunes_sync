#!/usr/bin/python

from pprint import pprint
import os
import pickle
from hashlib import md5
import config
import utils
from time import sleep
import sys
import shutil

hostname = utils.get_hostname()

BASE_FOLDER             = config.hosts[hostname]['base_folder']
TRANSFER_BASE_FOLDER    = config.transfer['transfer_base_folder']
TRANSFER_FOLDER         = os.path.join(BASE_FOLDER,TRANSFER_BASE_FOLDER)
ITUNES_FOLDER           = config.hosts[hostname]['itunes_folder']
BACKUP_FOLDERS          = config.hosts[hostname]['backup_folders']

INVENTORY_PICKLE = 'inventory.pickle'
NUM_TRIES = 5
WAIT_TIME = 5 * 60

for folder in os.listdir(TRANSFER_FOLDER):
    abs_folder = os.path.join(TRANSFER_FOLDER,folder)

    if not os.path.isdir(abs_folder):
        continue
    
    print abs_folder
    if os.path.exists(os.path.join(abs_folder,hostname + '.completed')):
        continue


    #TODO 'inventory.pickle' should be in the config, not hardcoded
    inventory_pickle = os.path.join(abs_folder, INVENTORY_PICKLE)
    
    tries = 0
    while not os.path.exists(inventory_pickle) and tries < NUM_TRIES:
        print "Can't find %s, tryihng again" % inventory_pickle
        sleep(WAIT_TIME)
        tries = tries + 1

    if tries == NUM_TRIES:
        print "Couldn't find %s, skipping" % inventory_pickle
        continue


    with file(inventory_pickle,'r') as f:
        inventory = pickle.load(f)

    tries = 0
    all_files_exist = False
    while not all_files_exist and tries < NUM_TRIES:
        unfound_files = []

        for filename,inv_md5,music_folder in inventory:
            if '.DS_Store' in filename:
                continue

            abs_filename = os.path.join(abs_folder,filename)
            all_files_exist = True

            if not os.path.exists(abs_filename):
                all_files_exist = False
                unfound_files.append(abs_filename)
                break

            with open(abs_filename,'rb') as fh:
                file_md5 = md5(fh.read()).hexdigest()

            if inv_md5 != file_md5:
                all_files_exist = False
                unfound_files.append(abs_filename)
                break

        sleep(WAIT_TIME)
        tries = tries + 1

    if tries == NUM_TRIES:
        print "Couldn't find %s, skipping" % '\n'.join(unfound_files)
        continue
    
    print "cp %s to %s " % (abs_folder,os.path.join(ITUNES_FOLDER,folder))
    ignore = shutil.ignore_patterns('*.jpg','*.pickle','*.completed')
    shutil.copytree(abs_folder, os.path.join(ITUNES_FOLDER,folder),ignore=ignore)

    for filename,inv_md5,music_folder in inventory:
        if '.DS_Store' in filename:
            continue

        abs_filename = os.path.join(abs_folder,filename)

        for backup_folder in BACKUP_FOLDERS:
            backup_music_filename = os.path.join(backup_folder,music_folder,filename)

            try:
                album_folder = os.path.dirname(backup_music_filename)
                print album_folder
                os.makedirs(album_folder)
            except:
                pass

            shutil.copy(abs_filename,backup_music_filename)
            print "cp to %s " % backup_music_filename

    with open(os.path.join(abs_folder,hostname + '.completed'),'w') as f:
        f.write('done')

with open(os.path.join(BASE_FOLDER, 'transfer.completed'),'w') as f:
    f.write('done')
