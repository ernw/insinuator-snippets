#!/bin/bash
WLCIP="udp6:[$IPv6]"
#WLCIP="$IPv4"
WLCUSER="$user"
WLCAUTH="$Passphrase"
WLCPASS="$Passphrase"
SNMPWALK=`which snmpwalk`




clientsA=0
clientsB=0
clientsG=0
clients24N=0
clients5N=0
#echo $SNMPWALK -v3 -u $WLCUSER -l authPriv -a sha -A $WLCAUTH -x aes -X $WLCPASS $WLCIP 1.3.6.1.4.1.14179.2.1.4.1.25
data=$($SNMPWALK -v3 -u $WLCUSER -l authPriv -a sha -A $WLCAUTH -x aes -X $WLCPASS $WLCIP 1.3.6.1.4.1.14179.2.1.4.1.25|awk -F ': ' '{ print $2 }')
for i in $data
do
	if test $i -eq 1; 
	then 
   		clientsA=$(echo $clientsA+1|bc)
	fi
	if test $i -eq 2;
	then
                clientsB=$(echo $clientsB+1|bc)
	fi
	if test $i -eq 3;
	then
                clientsG=$(echo $clientsG+1|bc)
	fi
	if test $i -eq 6;
	then
                clients24N=$(echo $clients24N+1|bc)
	fi
	if test $i -eq 7;
	then
                clients5N=$(echo $clients5N+1|bc)
	fi
done
echo $clientsA:$clientsB:$clientsG:$clients24N:$clients5N
