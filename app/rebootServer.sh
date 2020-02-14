#!/bin/bash

kill $(ps aux | grep 'flask' | awk '{print $2}')

./startup.sh -d -r

