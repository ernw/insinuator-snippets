# Retrieving system users with BMC BladeLogic RSCD agent (checked for v8.6.01.66)
# Copyright: ERNW

import socket
import ssl
import sys
import requests
import argparse
import xml.etree.ElementTree as ET
import httplib
from requests.packages.urllib3 import PoolManager
from requests.packages.urllib3.connection import HTTPConnection
from requests.packages.urllib3.connectionpool import HTTPConnectionPool
from requests.adapters import HTTPAdapter
        
class MyHTTPConnection(HTTPConnection):
    def __init__(self, unix_socket_url, timeout=60):
        HTTPConnection.__init__(self, HOST, timeout=timeout)
        self.unix_socket_url = unix_socket_url
        self.timeout = timeout

    def connect(self):
        self.sock = wrappedSocket


class MyHTTPConnectionPool(HTTPConnectionPool):
    def __init__(self, socket_path, timeout=60):
        HTTPConnectionPool.__init__(self, HOST, timeout=timeout)
        self.socket_path = socket_path
        self.timeout = timeout
        
    def _new_conn(self):
        return MyHTTPConnection(self.socket_path, self.timeout)


class MyAdapter(HTTPAdapter):
    def __init__(self, timeout=60):
        super(MyAdapter, self).__init__()
        self.timeout = timeout

    def get_connection(self, socket_path, proxies=None):
        return MyHTTPConnectionPool(socket_path, self.timeout)

    def request_url(self, request, proxies):
        return request.path_url


def optParser():
	parser = argparse.ArgumentParser(description="Retrieving system users with BMC BladeLogic Server Automation RSCD agent")
	parser.add_argument("host", help="IP address of a target system")
	parser.add_argument("-p", "--port", type=int, default=4750, help="TCP port (default: 4750)")
	opts=parser.parse_args()
	return opts

# Server introduction request
init = """<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>RemoteServer.intro</methodName><params><param><value>2015-11-19-16-10-30-3920958</value></param><param><value>7</value></param><param><value>0;0;21;AArverManagement_XXX_XXX:XXXXXXXX;2;CM;-;-;0;-;1;1;6;SYSTEM;CP1252;</value></param><param><value>8.6.01.66</value></param></params></methodCall>"""

getVersion="""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>RemoteServer.getVersion</methodName><params/></methodCall>"""

getUsers="""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>DAAL.getAssetChildrenStream</methodName><params><param><value><struct><member><name>typeName</name><value>BMC_UnixUsers</value></member><member><name>host</name><value>0.0.0.0</value></member><member><name>container</name><value><array><data><value><struct><member><name>string</name><value>IS_LIVE</value></member><member><name>value</name><value><struct><member><name>longValue</name><value><ex:i8>1</ex:i8></value></member><member><name>kind</name><value><i4>1</i4></value></member></struct></value></member></struct></value></data></array></value></member><member><name>path</name><value>/</value></member></struct></value></param><param><value><i4>1</i4></value></param><param><value><array><data/></array></value></param><param><value><array><data/></array></value></param><param><value><array><data/></array></value></param></params></methodCall>"""

getNext="""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>DAAL.assetStreamGetNext</methodName><params><param><value><struct><member><name>streamID</name><value><struct><member><name>sessionId</name><value><i4>2</i4></value></member></struct></value></member></struct></value></param><param><value><i4>100</i4></value></param></params></methodCall>"""

closeAsset="""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>DAAL.assetStreamClose</methodName><params><param><value><struct><member><name>streamID</name><value><struct><member><name>sessionId</name><value><i4>2</i4></value></member></struct></value></member></struct></value></param></params></methodCall>"""

getHostOverview="""<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>RemoteServer.getHostOverview</methodName></methodCall>"""

options=optParser()
PORT=options.port
HOST=options.host

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Initial packet which will trigger XMLRPC communication
sock.sendall("TLSRPC")

# Create TLS tunnel
wrappedSocket = ssl.wrap_socket(sock)

# Use our existing socket for all future HTTP requests
adapter = MyAdapter()
s = requests.session()
s.mount("http://", adapter)
#s.mount("https://", adapter)

print "Sending intro..."
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=init)
#print r.status_code
#print r.content
print "Getting version..."
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=getVersion)
#print r.status_code
#print r.content
rootVersion = ET.fromstring(r.content)
print "========================="
print "Major version   : " + rootVersion[0][0][0][0][0][1].text
print "Minor version   : " + rootVersion[0][0][0][0][1][1].text
print "Patch version   : " + rootVersion[0][0][0][0][2][1].text
print "Platform version: " + rootVersion[0][0][0][0][3][1].text
print "=========================\n"

print "Getting host overview..."
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=getHostOverview)
#print r.status_code
#print r.content
rootOverview = ET.fromstring(r.content)
print "=================================================="
print "Agent instal dir: " + rootOverview[0][0][0][0][ 0][1].text
print "Licensed?       : " + ("false" if (int(rootOverview[0][0][0][0][1][1][0].text) == 0) else "true")
print "Repeater?       : " + ("false" if (int(rootOverview[0][0][0][0][11][1][0].text) == 0) else "true")
print "Hostname        : " + rootOverview[0][0][0][0][ 5][1].text
print "Netmask         : " + rootOverview[0][0][0][0][12][1].text
print "CPU architecture: " + rootOverview[0][0][0][0][ 9][1].text
print "Platform (OS)   : " + rootOverview[0][0][0][0][13][1].text
print "OS version      : " + rootOverview[0][0][0][0][14][1].text
print "OS architecture : " + rootOverview[0][0][0][0][ 2][1].text
print "OS release      : " + rootOverview[0][0][0][0][10][1].text
print "Patch level     : " + rootOverview[0][0][0][0][ 6][1].text
print "==================================================\n"

print "Sending request for users...\n"
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=getUsers)
#print r.status_code
#print r.content
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=getNext)
#print r.status_code
with open("./users.xml", "w") as text_file:
	text_file.write(r.content)

r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=getNext)
#print r.status_code
#print r.content
r=s.post('http://'+HOST+':'+str(PORT)+'/xmlrpc',data=closeAsset)
#print r.status_code
#print r.content

# Parsing the response
# If parsing does not work correctly, the users' information still can be found in the saved users.xml file
root = ET.parse('./users.xml').getroot()
count=0
ind=1
while ind:
	try:
		ind=root[0][0][0][0][0][1][0][0][count][0][0][1][0][2][1].text
	except IndexError:
		pass
		break
	count+=1

print "Number of users found: " + str(count) + "\n"
#raw_input("Press [Enter] to print users...")


for i in range(0,count):
	print "User " + str(i) + ": " + root[0][0][0][0][0][1][0][0][i][0][0][1][0][2][1].text + "\n........................"
	print "home directory:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][0][0][1][1][0][1][1].text
	print "uid:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][11][0][1][1][0][1][1][0].text
	print "gid:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][3][0][1][1][0][1][1][0].text
	print "primaryGroupName:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][4][0][1][1][0][1][1].text
	try:	
		print "username:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][2][0][1][1][0][1][1].text
	except IndexError:
		pass
	try:
		print "shell:" + root[0][0][0][0][0][1][0][0][i][0][1][1][0][2][1][0][0][10][0][1][1][0][1][1].text
	except IndexError:
		pass
	print "........................\n"


wrappedSocket.close()
