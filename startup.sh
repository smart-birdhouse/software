#!/bin/bash

if [ $# -ge 3 ] 
then
	printf "Usage: ./startup.sh [-d] [-r]\nWhere:\n\t-d: Debug, starts server with control panel available to help aid remote development.\n\t-r: Remove Peripheral Connection, starts server without attempting to connect peripherals for server specific testing\n\n"
        exit 1
elif [ $1 == '-d' ]
then	
	echo "Starting server in debug mode..."
	export SERVER_DEBUG="TRUE"
	if [ $2 == '-r' ]
	then
		echo "Running server without peripheral connections"
		export SERVER_PERIPH="FALSE"
	fi
elif [ $1 == '-r' ]
then
	echo "Running server without peripheral connections"
	export SERVER_PERIPH="FALSE"
	if [ $2 == '-d' ]
	then
		echo "Starting server in debug mode..."
		export SERVER_DEBUG="TRUE"
	fi
else
	echo "Starting server"
fi

if [[ ! -f "/app/videos" ]]
	mkdir app/videos
fi
if [[ ! -f "/app/audio" ]]
	mkdir app/audio
fi
if [[ ! -f "/app/stats" ]]
	mkdir app/stats
fi

source venv/bin/activate
FLASK_APP=microblog.py
flask run --host=0.0.0.0
