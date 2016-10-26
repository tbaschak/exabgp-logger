#!/bin/sh

trap '' SIGINT

while true
do

  while read line
  do
    echo "$line" >> ../exabgp/bgp.log
  done < "${1:-/dev/stdin}"
