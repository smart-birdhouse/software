#!/bin/bash

if [ $# -ge 2 ] 
then
	printf "Usage: ./startup.sh [-d]\nWhere:\n\t-d: Debug, starts server with control panel available to help aid remote development.\n\n"
        exit 1
elif [ $1 == '-d' ]
then	
	echo "Starting server in debug mode..."
	export SERVER_DEBUG="TRUE"
else
	echo "Starting server"
fi

mkdir app/videos
mkdir app/audio
mkdir app/stats

source venv/bin/activate
FLASK_APP=microblog.py
flask run --host=0.0.0.0
