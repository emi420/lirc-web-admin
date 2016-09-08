#!/usr/bin/python
# -*- coding: utf-8 -*-

''' 
 LIRC Web Server - a web server for LIRC administration 

 You may use any Web Server Admin project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2016 Emilio Mariscal (emi420 [at] gmail.com)
 
 
'''
from irrecord import IRRecord
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

'''
APIServer create a simple web server for administration
'''
class APIServer(BaseHTTPRequestHandler):

    irrecord = None

    def get_mime(self):
        if self.path.endswith(".png"):
            return "image/png"
        elif self.path.endswith(".jpg"):           
            return "image/jpeg"
        elif self.path.endswith(".js"):           
            return "text/javascript"
        elif self.path.endswith(".css"):           
            return "text/css"
        elif self.path.endswith(".html"):           
            return "text/html"
        elif self.path.endswith("/"):           
            return "text/html"
        else:           
            return "application/octet-stream"        


    def do_GET(self):
               
        try:
            self.send_response(200)
            self.send_header("Content-type", self.get_mime())
            self.send_header('Allow', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            if self.path == "/":
                self.path = "/index.html"

            if self.path == "/ws/irrecord/":
                if self.irrecord.launched:
                    self.irrecord.kill()
                self.wfile.write(self.irrecord.launch())
            elif self.path.startswith("/ws/irrecord/"):
                if self.path == "/ws/irrecord/get-last-config/":
                    self.wfile.write(self.irrecord.get_last_config())
                elif self.path == "/ws/irrecord/get-namespace/":
                    self.wfile.write(self.irrecord.get_namespace())
                elif self.path == "/ws/irrecord/mode2/":
                    self.wfile.write(self.irrecord.mode2())
                else:
                    if not self.irrecord.launched:
                        self.wfile.write("")
                    else:
                        if self.path == "/ws/irrecord/enter/":
                            self.wfile.write(self.irrecord.enter())
                        elif self.path == "/ws/irrecord/status/":
                            self.wfile.write(self.irrecord.status())
                        elif self.path.endswith("/send/"):
                            split_path = self.path.split('/');
                            command = split_path[len(split_path)-3]
                            self.wfile.write(self.irrecord.send(command))
                        elif self.path == "/ws/irrecord/kill/":
                            self.wfile.write(self.irrecord.kill())
                
            else:
                f = open(curdir + sep + self.path, 'r') 
                self.wfile.write(f.read())
                f.close()

            return

        except IOError:
            pass
            #self.send_error(404,'File Not Found: %s' % self.path)        

class http_server:
    def __init__(self, irrecord):
        try:
            APIServer.irrecord = IRRecord()
            server = HTTPServer(('', 8001), APIServer)
            print 'Started LIRC Web Server on port 8001' 
            server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            server.socket.close()

class main:
    def __init__(self):
        self.irrecord = IRRecord()
        self.server = http_server(self.irrecord)

if __name__ == '__main__':
    m = main()
