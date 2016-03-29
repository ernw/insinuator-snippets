#!/bin/bash
ROUTERIP="udp6:[$IPv6]"
#ROUTERIP="$IPv4"
ROUTERUSER="$user"
ROUTERAUTH="$Passphrase"
ROUTERPASS="$Passphrase"
VLAN10="8"
VLAN20="9"
VLAN30="10"
VLAN40="12"
COUNTER="0"
SNMPWALK=`which snmpwalk`

#VLAN 20 is egal

if [ "$1" = "arp_v10-old" ]; then
  data_vlan10=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.22.1.2.$VLAN10 |awk -F ': ' '{ print $2 }')
  #echo "VLAN10"
  echo $data_vlan10
fi
if [ "$1" = "arp_v10" ]; then
  data_vlan10=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN10.ipv4 |awk -F ': ' '{ print $2 }')
  #echo "VLAN10"
  echo $data_vlan10
fi
if [ "$1" = "arp_v30" ]; then
  data_vlan30=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.22.1.2.$VLAN30 |awk -F ': ' '{ print $2 }')
  #echo "VLAN30"
  echo $data_vlan30
fi
if [ "$1" = "arp_v20" ]; then
  data_vlan20=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.22.1.2.$VLAN20 |awk -F ': ' '{ print $2 }')
  #echo "VLAN20"
  echo $data_vlan20
fi
if [ "$1" = "arp_v40" ]; then
  data_vlan40=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN40.ipv4 |awk -F ': ' '{ print $2 }')
  #echo "VLAN40"
  echo $data_vlan40
fi

if [ "$1" = "nbc_v10" ]; then
  data_vlan10=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN10.ipv6 |awk -F ': ' '{ print $2 }')
  echo $data_vlan10
fi
if [ "$1" = "nbc_v30" ]; then
  data_vlan30=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN30.ipv6 |awk -F ': ' '{ print $2 }')
  echo $data_vlan30
fi
if [ "$1" = "nbc_v30_2" ]; then
  $SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN30.ipv6
fi
if [ "$1" = "nbc_v20" ]; then
  data_vlan20=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN20.ipv6 |awk -F ': ' '{ print $2 }')
  echo $data_vlan20
fi
if [ "$1" = "nbc_v40" ]; then
  data_vlan40=$($SNMPWALK -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP 1.3.6.1.2.1.4.35.1.4.$VLAN40.ipv6 |awk -F ': ' '{ print $2 }')
  echo $data_vlan40
fi
  #$ROUTERINT1 #|awk -F ': ' '{ print $2 }'
  #snmpwalk -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP .1.3.6.1.2.1.4.29 #.1.6 #$ROUTERINT1 #|awk -F ': ' '{ print $2 }'
  #snmpwalk -v3 -u $ROUTERUSER -l authPriv -a sha -A $ROUTERAUTH -x aes -X $ROUTERPASS $ROUTERIP .1.3.6.1.2.1.4.30 #.1.6 #$ROUTERINT1 #|awk -F ': ' '{ print $2 }'
