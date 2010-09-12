#!/bin/bash

music_transfer_dir="/Library/Application Support/Music Transfer"

mkdir -p "$music_transfer_dir"
cp app/__init__.py "$music_transfer_dir"
cp app/config.py "$music_transfer_dir"
cp app/utils.py "$music_transfer_dir"
cp app/file_monitor.py "$music_transfer_dir"

sudo ./setup_launch_agents.py
