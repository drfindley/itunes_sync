#!/usr/bin/python 

import app.config as config
import app.utils as utils
import os
import sys

if not utils.is_root():
    print "This must be run as root"
    sys.exit(1)

hostname = utils.get_hostname()



file_monitor_agent = '/Library/LaunchAgents/com.adam.music_transfer.file_monitor.plist'

utils.unload_agent(file_monitor_agent)

monitor_base_folder = config.monitor['monitor_base_folder']
base_folder = config.hosts[hostname]['base_folder']


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
<string>com.adam.music_transfer.file_monitor</string>

<key>ProgramArguments</key>
<array>
   <string>/Library/Application Support/Music Transfer/file_monitor.py</string>
</array>

<key>WatchPaths</key>
<array>
%s</array>

</dict>
</plist>
""" % (paths)


with open(file_monitor_agent,'w') as f:
    f.write(file_monitor_plist)

utils.load_agent(file_monitor_agent)
