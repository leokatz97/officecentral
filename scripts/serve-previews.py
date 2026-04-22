#!/usr/bin/env python3
"""Static HTTP server for the Office Central preview HTML files.

Uses an absolute chdir before importing http.server to avoid the
argparse `default=os.getcwd()` eager-evaluation failure under the
Claude Code sandbox.
"""
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'previews'))

import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print(f"Serving {os.getcwd()} at http://localhost:{PORT}/")
    print("Previews available:")
    for name in sorted(os.listdir(".")):
        if name.endswith(".html"):
            print(f"  http://localhost:{PORT}/{name}")
    httpd.serve_forever()
