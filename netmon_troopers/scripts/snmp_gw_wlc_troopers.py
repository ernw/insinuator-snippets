#!/usr/bin/python
import os
import argparse

def vlan10(clients="all"):
  #ARP
  arp_vlan10=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh arp_v10").read()
  tmp_table_vlan10_v4=(arp_vlan10).split()
  tmp_table_vlan10_v4.sort()
  table_vlan10_v4=set(tmp_table_vlan10_v4)
  tmp_c_vlan10_v4=len(table_vlan10_v4)

  #NBC"
  nbc_vlan10=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v10").read()
  tmp_table_vlan10_v6=(nbc_vlan10).split()
  tmp_table_vlan10_v6.sort()
  table_vlan10_v6=set(tmp_table_vlan10_v6)
  tmp_c_vlan10_v6=len(table_vlan10_v6)

  #dualstack
  setv4_vlan10=set(table_vlan10_v4)
  setv6_vlan10=set(table_vlan10_v6)
  table_vlan10_v4_v6=setv4_vlan10.intersection(setv6_vlan10)
  c_vlan10_v4_v6=len(table_vlan10_v4_v6)

  c_vlan10_v4 = tmp_c_vlan10_v4 - c_vlan10_v4_v6
  c_vlan10_v6 = tmp_c_vlan10_v6 - c_vlan10_v4_v6

  #clientv4 ; #clientv4_v6 ; #clientv6
  if clients == "all":
    return c_vlan10_v4 + c_vlan10_v4_v6 + c_vlan10_v6
  elif clients == "ipv4only":
    return c_vlan10_v4
  elif clients == "ipv6only":
    return c_vlan10_v6
  elif clients == "dualstack":
    return c_vlan10_v4_v6
  elif clients == "collectd":
    return [c_vlan10_v4, c_vlan10_v4_v6, c_vlan10_v6]

#Both Public VLANs
def vlan10_30(clients="all"):
  #ARP
  arp_vlan10=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh arp_v10").read()
  tmp_table_vlan10_v4=(arp_vlan10).split()
  tmp_table_vlan10_v4.sort()
  table_vlan10_v4=set(tmp_table_vlan10_v4)
  tmp_c_vlan10_v4=len(table_vlan10_v4)

  #NBC
  nbc_vlan10=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v10").read()
  nbc_vlan30=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v30").read()
  tmp_table_vlan10_30_v6=(nbc_vlan10).split()
  tmp_table_vlan30_v6=(nbc_vlan30).split()
  tmp_table_vlan10_30_v6.extend(tmp_table_vlan30_v6)
  tmp_table_vlan10_30_v6.sort()
  table_vlan10_30_v6=set(tmp_table_vlan10_30_v6)
  tmp_c_vlan10_30_v6=len(table_vlan10_30_v6)

  #dualstack
  setv4_vlan10=set(table_vlan10_v4)
  setv6_vlan10_30=set(table_vlan10_30_v6)
  table_vlan10_30_v4_v6=setv4_vlan10.intersection(setv6_vlan10_30)
  c_vlan10_30_v4_v6=len(table_vlan10_30_v4_v6)

  c_vlan10_v4 = tmp_c_vlan10_v4 - c_vlan10_30_v4_v6
  c_vlan10_30_v6 = tmp_c_vlan10_30_v6 - c_vlan10_30_v4_v6

  #clientv4 ; #clientv4_v6 ; #clientv6
  if clients == "all":
    return c_vlan10_v4 + c_vlan10_30_v4_v6 + c_vlan10_30_v6
  elif clients == "ipv4only":
    return c_vlan10_v4
  elif clients == "ipv6only":
    return c_vlan10_30_v6
  elif clients == "dualstack":
    return c_vlan10_30_v4_v6
  elif clients == "collectd":
    return [c_vlan10_v4, c_vlan10_30_v4_v6, c_vlan10_30_v6]


def vlan20(clients="all"):
  #ARP
  arp_vlan20=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh arp_v20").read()
  tmp_table_vlan20_v4=(arp_vlan20).split()
  tmp_table_vlan20_v4.sort()
  table_vlan20_v4=set(tmp_table_vlan20_v4)
  tmp_c_vlan20_v4=len(table_vlan20_v4)

  #NBC
  nbc_vlan20=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v20").read()
  tmp_table_vlan20_v6=(nbc_vlan20).split()
  tmp_table_vlan20_v6.sort()
  table_vlan20_v6=set(tmp_table_vlan20_v6)
  tmp_c_vlan20_v6=len(table_vlan20_v6)

  #dualstack
  setv4_vlan20=set(table_vlan20_v4)
  setv6_vlan20=set(table_vlan20_v6)
  table_vlan20_v4_v6=setv4_vlan20.intersection(setv6_vlan20)
  c_vlan20_v4_v6=len(table_vlan20_v4_v6)

  c_vlan20_v4 = tmp_c_vlan20_v4 - c_vlan20_v4_v6
  c_vlan20_v6 = tmp_c_vlan20_v6 - c_vlan20_v4_v6

  #clientv4 ; #clientv4_v6 ; #clientv6
  if clients == "all":
    return c_vlan20_v4 + c_vlan20_v4_v6 + c_vlan20_v6
  elif clients == "ipv4only":
    return c_vlan20_v4
  elif clients == "ipv6only":
    return c_vlan20_v6
  elif clients == "dualstack":
    return c_vlan20_v4_v6
  elif clients == "collectd":
    return [c_vlan20_v4, c_vlan20_v4_v6, c_vlan20_v6]

def vlan30(clients="all"):
  #ARP
  #should retrun 0
  arp_vlan30=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh arp_v30").read()
  tmp_table_vlan30_v4=(arp_vlan30).split()
  tmp_table_vlan30_v4.sort()
  table_vlan30_v4=set(tmp_table_vlan30_v4)
  tmp_c_vlan30_v4=len(table_vlan30_v4)

  #NBC
  nbc_vlan30=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v30").read()
  tmp_table_vlan30_v6=(nbc_vlan30).split()
  tmp_table_vlan30_v6.sort()
  table_vlan30_v6=set(tmp_table_vlan30_v6)
  tmp_c_vlan30_v6=len(table_vlan30_v6)

  #dualstack
  setv4_vlan30=set(table_vlan30_v4)
  setv6_vlan30=set(table_vlan30_v6)
  table_vlan30_v4_v6=setv4_vlan30.intersection(setv6_vlan30)
  c_vlan30_v4_v6=len(table_vlan30_v4_v6)

  c_vlan30_v4 = tmp_c_vlan30_v4 - c_vlan30_v4_v6
  c_vlan30_v6 = tmp_c_vlan30_v6 - c_vlan30_v4_v6

  return c_vlan30_v6



def vlan40(clients="all"):
  #ARP
  arp_vlan40=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh arp_v40").read()
  tmp_table_vlan40_v4=(arp_vlan40).split()
  tmp_table_vlan40_v4.sort()
  table_vlan40_v4=set(tmp_table_vlan40_v4)
  tmp_c_vlan40_v4=len(table_vlan40_v4)

  #NBC
  nbc_vlan40=os.popen("sh /home/$user/scripts/cisco_arp_nbc.sh nbc_v40").read()
  tmp_table_vlan40_v6=(nbc_vlan40).split()
  tmp_table_vlan40_v6.sort()
  table_vlan40_v6=set(tmp_table_vlan40_v6)
  tmp_c_vlan40_v6=len(table_vlan40_v6)

  #dualstack
  setv4_vlan40=set(table_vlan40_v4)
  setv6_vlan40=set(table_vlan40_v6)
  table_vlan40_v4_v6=setv4_vlan40.intersection(setv6_vlan40)
  c_vlan40_v4_v6=len(table_vlan40_v4_v6)

  c_vlan40_v4 = tmp_c_vlan40_v4 - c_vlan40_v4_v6
  c_vlan40_v6 = tmp_c_vlan40_v6 - c_vlan40_v4_v6

  #clientv4 ; #clientv4_v6 ; #clientv6
  if clients == "all":
    return c_vlan40_v4 + c_vlan10_v4_v6 + c_vlan10_v6
  elif clients == "ipv4only":
    return c_vlan40_v4
  elif clients == "ipv6only":
    return c_vlan40_v6
  elif clients == "dualstack":
    return c_vlan40_v4_v6
  elif clients == "collectd":
    return [c_vlan40_v4, c_vlan40_v4_v6, c_vlan40_v6]


def bands(output="all"):
  wlc_bands = os.popen("sh /home/$user/scripts/cisco_wlc_bands.sh").read()
  wlc_bands_a = int(wlc_bands.split(":")[0])
  wlc_bands_b = int(wlc_bands.split(":")[1])
  wlc_bands_g = int(wlc_bands.split(":")[2])
  wlc_bands_n24 = int(wlc_bands.split(":")[3])
  wlc_bands_n5 = int(wlc_bands.split(":")[4])
  if output == "all":
    return wlc_bands_a + wlc_bands_b + wlc_bands_g + wlc_bands_n24 + wlc_bands_n5
  elif output == "dot11a":
    return wlc_bands_a
  elif output == "dot11g":
    return wlc_bands_g
  elif output == "dot11n24":
    return wlc_bands_n24
  elif output == "dot11n5":
    return wlc_bands_n5
  elif output == "collectd":
    return [wlc_bands_a, wlc_bands_b, wlc_bands_g, wlc_bands_n24, wlc_bands_n5]

#####
#MAIN#
#####

parser = argparse.ArgumentParser()
parser.add_argument("vlan", help="client vlan or bands" )
args = parser.parse_args()

#if len(optionen) != 1:
#    parser.error("Es wird eine Option erwartet")

if args.vlan == "ipv4only":
  print(vlan10(clients="ipv4only"))
elif args.vlan == "dualstack":
  print(vlan10(clients="dualstack"))
elif args.vlan == "ipv6only":
  print(vlan10(clients="ipv6only") + vlan30())
elif args.vlan == "vlan40":
  print(vlan40(clients="all"))
elif args.vlan == "vlan30":
  print(vlan30())
elif args.vlan == "vlan20":
  print(vlan20(clients="all"))
elif args.vlan == "collectd":
  #vlan10
  #vlan10_return = vlan10(clients="collectd")
  vlan10_30_return = vlan10_30(clients="collectd")
  print('PUTVAL gw.troopers.net/clients/ipv4only N:{0}'.format(vlan10_30_return[0]))
  print('PUTVAL gw.troopers.net/clients/dualstack N:{0}'.format(vlan10_30_return[1]))
  print('PUTVAL gw.troopers.net/clients/ipv6only N:{0}'.format(vlan10_30_return[2]))
  #vlan20
  vlan20_return = vlan20(clients="collectd")
  print('PUTVAL gw.troopers.net/clients_vlan20/ipv4only N:{0}'.format(vlan20_return[0]))
  print('PUTVAL gw.troopers.net/clients_vlan20/dualstack N:{0}'.format(vlan20_return[1]))
  print('PUTVAL gw.troopers.net/clients_vlan20/ipv6only N:{0}'.format(vlan20_return[2]))
  #vlan30
  print('PUTVAL gw.troopers.net/clients_vlan30/ipv6only N:{0}'.format(vlan30()))
  #vlan40
  vlan40_return = vlan40(clients="collectd")
  print('PUTVAL gw.troopers.net/clients_vlan40/ipv4only N:{0}'.format(vlan40_return[0]))
  print('PUTVAL gw.troopers.net/clients_vlan40/dualstack N:{0}'.format(vlan40_return[1]))
  print('PUTVAL gw.troopers.net/clients_vlan40/ipv6only N:{0}'.format(vlan40_return[2]))
  #bands
  bands_return = bands(output="collectd")
  print('PUTVAL wlc.troopers.net/wlc_bands/dot11a N:{0}'.format(bands_return[0]))
  print('PUTVAL wlc.troopers.net/wlc_bands/dot11b N:{0}'.format(bands_return[1]))
  print('PUTVAL wlc.troopers.net/wlc_bands/dot11g N:{0}'.format(bands_return[2]))
  print('PUTVAL wlc.troopers.net/wlc_bands/dot11n24 N:{0}'.format(bands_return[3]))
  print('PUTVAL wlc.troopers.net/wlc_bands/dot11n5 N:{0}'.format(bands_return[4]))
elif args.vlan == "bands":
  print(bands(output="all"))
elif args.vlan == "bands2":
  bands_return = bands(output="collectd")
  print('dot11a:{0}'.format(bands_return[0]))
  print('dot11g:{0}'.format(bands_return[1]))
  print('dot11n24:{0}'.format(bands_return[2]))
  print('dot11n5:{0}'.format(bands_return[3]))
  print('------------')
  print('all: {0}'.format(sum(bands_return)))

exit()
