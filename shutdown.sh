#!/bin/bash

PID="$(ps aux | grep isopalavial_interface.py | grep -v grep | awk '{print $2}')"
if [ ! -z "$PID" ]; then
    echo "⚡ Shutting down Isopalavial Interface"
    kill -SIGTERM $PID
else
    echo "☠️  Isopalavial Interface already offline"
fi

PID="$(ps aux | grep firomactal_drive.py | grep -v grep | awk '{print $2}')"
if [ ! -z "$PID" ]; then
    echo "⚡ Shutting down Firomactal Drive"
    kill -SIGTERM $PID
else
    echo "☠️  Firomactal Drive already offline"
fi

PID="$(ps aux | grep ramistat_core.py | grep -v grep | awk '{print $2}')"
if [ ! -z "$PID" ]; then
    echo "⚡ Shutting down Ramistat Core"
    kill -SIGTERM $PID
else
    echo "☠️  Ramistat Core already offline"
fi
