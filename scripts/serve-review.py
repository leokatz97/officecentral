"""
Tiny localhost HTTP server that captures the approval JSON posted by the
review HTML page (rendered by scripts/render-image-review.py).

On a successful POST to /submit, writes
  data/reports/approval-{date}-batch-{N}.json
with shape:
  {
    "batch": "<batch>",
    "submitted_at": "<iso ts>",
    "approvals": { "<handle>": {"gen2": bool, "gen3": bool, "gen4": bool, "comment2": str, "comment3": str, "comment4": str}, ... }
  }

Then shuts itself down.

Usage:
  python3 scripts/serve-review.py --batch=pilot-5
  python3 scripts/serve-review.py --batch=pilot-20 --port=8765
"""
import json
import os
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPT_DIR = os.path.join(ROOT, 'data', 'reports')

DEFAULT_PORT = 8765


def parse_args():
    batch = None
    port  = DEFAULT_PORT
    for arg in sys.argv[1:]:
        if arg.startswith('--batch='):
            batch = arg.split('=', 1)[1]
        elif arg.startswith('--port='):
            port = int(arg.split('=', 1)[1])
    if not batch:
        sys.exit('Required: --batch=<name>')
    return batch, port


SHUTDOWN_FLAG = threading.Event()


def make_handler(batch):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            sys.stderr.write('  ' + fmt % args + '\n')

        def _cors_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors_headers()
            self.end_headers()

        def do_POST(self):
            if self.path != '/submit':
                self.send_response(404)
                self._cors_headers()
                self.end_headers()
                return
            length = int(self.headers.get('Content-Length', 0))
            try:
                body = self.rfile.read(length).decode()
                data = json.loads(body)
            except Exception as e:
                self.send_response(400)
                self._cors_headers()
                self.end_headers()
                self.wfile.write(b'invalid json: ' + str(e).encode())
                return

            output = {
                'batch':        data.get('batch') or batch,
                'submitted_at': datetime.now().isoformat(),
                'approvals':    data.get('approvals', {}),
            }

            os.makedirs(RPT_DIR, exist_ok=True)
            out_path = os.path.join(RPT_DIR, 'approval-{}.json'.format(batch))
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)

            n = len(output['approvals'])
            approved = sum(1 for v in output['approvals'].values() for k in ('pos2', 'pos3', 'pos4') if v.get(k))
            print()
            print('=' * 60)
            print('Approval received: batch={}, products={}, approved={}'.format(batch, n, approved))
            print('Wrote: {}'.format(out_path))
            print('=' * 60)

            self.send_response(200)
            self._cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'path': out_path}).encode())

            threading.Thread(target=lambda: (time.sleep(0.5), SHUTDOWN_FLAG.set()), daemon=True).start()

    return Handler


def main():
    batch, port = parse_args()
    server = HTTPServer(('127.0.0.1', port), make_handler(batch))
    print('serve-review listening on http://127.0.0.1:{}/submit  (batch={})'.format(port, batch))
    print('Open the rendered HTML and click Submit when done.')

    while not SHUTDOWN_FLAG.is_set():
        server.handle_request()

    print('Done. Server stopped.')


if __name__ == '__main__':
    main()
