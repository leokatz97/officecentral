#!/usr/bin/env python3
import os, http.server, socketserver

os.chdir(os.path.join(os.path.dirname(__file__), '..', 'previews'))
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('localhost', 8080), http.server.SimpleHTTPRequestHandler)
print('Serving http://localhost:8080/')
httpd.serve_forever()
