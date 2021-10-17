#!/usr/bin/env bash

source ./venv/bin/activate
python WatchLivestream.py credentials.json &
sleep 60
python WatchLivestream.py credentials2.json &