#!/usr/bin/env python

import os
import sys
import time
import json
import pymysql
import IPy

# When the parent dies we are seeing continual newlines, so we only access so many before stopping
counter = 0


conn = pymysql.connect(
    host='mysql',
    user='bgpdb',
    passwd='password',
    db='bgpdb',
)
cur = conn.cursor()


def communitiesListToStr(com):
    returnstr = ""
    for community in com:
        returnstr += "%s:%s " % (community[0], community[1])
    return returnstr.rstrip()

def aspathListToStr(asp):
    returnstr = ""
    for asn in asp:
        returnstr += "%s " % (asn)
    return returnstr.rstrip()

def lineToMysql(oneline):
    data = json.loads(oneline)

    if data['type'] == 'update':
        try:
            if data['neighbor']['message']['update']['announce']:
                neighborip = data['neighbor']['ip']
                neighborasn = data['neighbor']['asn']['peer']
                aspath = data['neighbor']['message']['update']['attribute']['as-path']
                sourceasn = aspath[-1]
                aspath = aspathListToStr(aspath)
                community = communitiesListToStr(data['neighbor']['message']['update']['attribute']['community'])
                update = data['neighbor']['message']['update']
                for addressfamily in update['announce']:
                    for nexthop in update['announce'][addressfamily]:
                        if IPy.IP(nexthop)._ipversion == 6:
                            if IPy.IP(nexthop) > IPy.IP('fe80::') and IPy.IP(nexthop) < IPy.IP('febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff'):
                                # do nothing
                                pass
                            else:
                                for prefix in update['announce'][addressfamily][nexthop]:
                                    network = IPy.IP(prefix).net().strCompressed()
                                    netmask = IPy.IP(prefix).netmask().strCompressed()
                                    sqlinsert = """
INSERT INTO updatelog VALUES (NULL, now(), '%s', 'announce', '%s', INET6_ATON('%s'), INET6_ATON('%s'), '%s', %d, '%s')
                                    """ % (neighborip, prefix, network, netmask, aspath, sourceasn, community)
                                    #print sqlinsert
                                    cur.execute(sqlinsert)
                        else: # if ipv4
                            for prefix in update['announce'][addressfamily][nexthop]:
                                network = IPy.IP(prefix).net().strCompressed()
                                netmask = IPy.IP(prefix).netmask().strCompressed()
                                sqlinsert = """
INSERT INTO updatelog VALUES (NULL, now(), '%s', 'announce', '%s', INET6_ATON('%s'), INET6_ATON('%s'), '%s', %d, '%s')
                                """ % (neighborip, prefix, network, netmask, aspath, sourceasn, community)
                                #print sqlinsert
                                cur.execute(sqlinsert)                        
                #conn.commit()
        except KeyError:
            pass
            #print("Debug: no announcements found")

        try:
            if data['neighbor']['message']['update']['withdraw']:
                neighborip = data['neighbor']['ip']
                update = data['neighbor']['message']['update']
                for addressfamily in update['withdraw']:
                    for prefix in update['withdraw'][addressfamily]:
                        network = IPy.IP(prefix).net().strCompressed()
                        netmask = IPy.IP(prefix).netmask().strCompressed()
                        sqlinsert = """
INSERT INTO updatelog VALUES (NULL, now(), '%s', 'withdraw', '%s', INET6_ATON('%s'), INET6_ATON('%s'), '', NULL, '');
                        """ % (neighborip, prefix, network, netmask)
                        #print sqlinsert
                        cur.execute(sqlinsert)
                #conn.commit()
        except KeyError:
            pass
            #print("Debug: no withdrawals found")
    conn.commit()


while True:
    try:
        line = sys.stdin.readline().strip()
        if line == "":
            counter += 1
            if counter > 100:
                break
            continue

        counter = 0

        lineToMysql(line)
        #conn.commit()
    except KeyboardInterrupt:
        pass
    except IOError:
        # most likely a signal during readline
        pass

