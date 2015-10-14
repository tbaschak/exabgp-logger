#!/bin/sh
#
OURDIR="/path/to/exabgp-logger"
cd $OURDIR/bin

env exabgp.daemon.daemonize=true \
 exabgp.daemon.pid=$OURDIR/exabgp/exabgp.pid \
 exabgp.daemon.user=theo \
 exabgp.tcp.bind="" \
 exabgp.tcp.port="179" \
 exabgp.log.enable=true \
 exabgp.log.all=false \
 exabgp.log.destination=$OURDIR/exabgp/exabgp.log \
 exabgp.cache.attributes=false \
 exabgp.cache.nexthops=false \
 exabgp $OURDIR/exabgp/exabgp.conf
 
