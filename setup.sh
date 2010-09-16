#!/bin/bash

itunes_sync_dir="/Library/Application Support/itunes_sync"

mkdir -p "$itunes_sync_dir"
cp app/__init__.py "$itunes_sync_dir"
cp app/config.py "$itunes_sync_dir"
cp app/utils.py "$itunes_sync_dir"
cp app/file_monitor.py "$itunes_sync_dir"
cp app/music_transfer.py "$itunes_sync_dir"
cp app/cleanup.py "$itunes_sync_dir"

sudo ./setup_launch_agents.py
