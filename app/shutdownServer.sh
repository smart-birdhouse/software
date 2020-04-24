#!/bin/bash

kill $(ps aux | grep 'startup.sh' | awk '{print $2}')
kill $(ps aux | grep 'flask' | awk '{print $2}')
