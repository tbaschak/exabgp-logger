#!/bin/sh

trap '' SIGINT

while true
do

  while read line
  do
    logger -t bgplogger -i "$line" 
  done < "${1:-/dev/stdin}"
