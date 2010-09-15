#!/usr/bin/python 

import app.config as config
import app.utils as utils
import os
import sys

if not utils.is_root():
    print "This must be run as root"
    sys.exit(1)

hostname = utils.get_hostname()


file_monitor_agent = '/Library/LaunchAgents/com.adam.itunes_sync.file_monitor.plist'
music_transfer_agent = '/Library/LaunchAgents/com.adam.itunes_sync.music_transfer.plist'

try:
    utils.unload_agent(file_monitor_agent)
    utils.unload_agent(music_transfer)
except:
    pass

monitor_base_folder = config.monitor['monitor_base_folder']
base_folder = config.hosts[hostname]['base_folder']

# FILE MONITOR
paths = ""

for monitor_folder in config.hosts[hostname]['monitor_folders']:
    paths = paths + "    <string>%s</string>\n" % \
        os.path.join(base_folder,monitor_base_folder,monitor_folder)

file_monitor_plist = """
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>com.adam.itunes_sync.file_monitor</string>

<key>ProgramArguments</key>
<array>
   <string>/Library/Application Support/itunes_sync/file_monitor.py</string>
</array>

<key>WatchPaths</key>
<array>
%s</array>

</dict>
</plist>
""" % (paths)

with open(file_monitor_agent,'w') as f:
    f.write(file_monitor_plist)


# MUSIC TRANSFER
path = os.path.join(base_folder, 'monitor.completed')

music_transfer_plist = """
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>com.adam.itunes_sync.music_transfer</string>

<key>ProgramArguments</key>
<array>
   <string>/Library/Application Support/itunes_sync/music_transfer.py</string>
</array>

<key>WatchPaths</key>
<array>
<string>%s</string>
</array>

</dict>
</plist>
""" % (path)

with open(music_transfer_agent,'w') as f:
    f.write(music_transfer_plist)

utils.load_agent(file_monitor_agent)
utils.load_agent(music_transfer_agent)
