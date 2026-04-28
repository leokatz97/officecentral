"""Simple static server for the previews/ directory."""
import http.server
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEWS = os.path.join(ROOT, 'previews')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PREVIEWS, **kwargs)
    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 8080), Handler)
    print('Serving previews/ on http://localhost:8080')
    server.serve_forever()
