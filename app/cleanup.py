#!/usr/bin/python

import sys
import config
import utils
import os
import shutil

hostname = utils.get_hostname()

BASE_FOLDER             = config.hosts[hostname]['base_folder']
TRANSFER_BASE_FOLDER    = config.transfer['transfer_base_folder']
TRANSFER_FOLDER         = os.path.join(BASE_FOLDER,TRANSFER_BASE_FOLDER)

hosts_completed         = [ os.path.join(host + '.completed') for host in config.hosts.keys()]

#print hosts_completed

for folder in os.listdir(TRANSFER_FOLDER):
    abs_folder = os.path.join(TRANSFER_FOLDER,folder)
    if not os.path.isdir(abs_folder):
        continue

    all_exists = True
    for host_completed in hosts_completed:
        abs_host_copmleted = os.path.join(abs_folder,host_completed)
        if not os.path.exists(abs_host_copmleted):
            all_exists = False

    if all_exists:
        print "delete %s" % abs_host_copmleted
        shutil.rmtree(abs_folder)
