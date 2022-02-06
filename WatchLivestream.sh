#!/usr/bin/env bash

source ./venv/bin/activate
python WatchLivestream.py credentials2.json &
sleep 120
python WatchLivestream.py credentials.json &
sleep infinity