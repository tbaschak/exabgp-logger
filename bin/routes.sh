#!/bin/sh

trap '' SIGINT

while true
do

  while read line
  do
    curl -s -d "$line" -X POST -H "Content-Type: application/json" \
      http://localhost:5984/bgproutes >/dev/null
  done < "${1:-/dev/stdin}"

done
