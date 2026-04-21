import http.server
import socketserver
import urllib.parse
import urllib.request
import secrets
import webbrowser
import json
import sys

import os
CLIENT_ID = os.environ['SHOPIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SHOPIFY_CLIENT_SECRET']
STORE = 'office-central-online.myshopify.com'
SCOPES = 'read_products,write_products,read_orders,read_all_orders,read_customers,read_themes,write_themes,read_online_store_navigation,write_online_store_navigation'
REDIRECT_URI = 'http://localhost:3000/callback'

state = secrets.token_hex(16)
auth_url = (
    f'https://{STORE}/admin/oauth/authorize'
    f'?client_id={CLIENT_ID}'
    f'&scope={SCOPES}'
    f'&redirect_uri={urllib.parse.quote(REDIRECT_URI)}'
    f'&state={state}'
)

token_holder = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != '/callback':
            self.send_response(404)
            self.end_headers()
            return

        params = urllib.parse.parse_qs(parsed.query)
        returned_state = params.get('state', [''])[0]
        code = params.get('code', [''])[0]

        if returned_state != state:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'State mismatch.')
            token_holder['error'] = 'state mismatch'
            return

        data = urllib.parse.urlencode({
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
        }).encode()

        req = urllib.request.Request(
            f'https://{STORE}/admin/oauth/access_token',
            data=data,
            method='POST',
        )

        try:
            with urllib.request.urlopen(req) as resp:
                body = json.loads(resp.read().decode())
                token = body.get('access_token')
                if token:
                    token_holder['token'] = token
                    with open('.env', 'w') as f:
                        f.write(f'SHOPIFY_TOKEN={token}\n')
                        f.write(f'SHOPIFY_STORE={STORE}\n')
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<h1>Connected! You can close this tab.</h1>')
                else:
                    token_holder['error'] = json.dumps(body)
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b'Error - see terminal.')
        except Exception as e:
            token_holder['error'] = str(e)
            self.send_response(500)
            self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('localhost', 3000), Handler) as httpd:
    print(f'Opening: {auth_url}')
    webbrowser.open(auth_url)
    print('Waiting for callback...')
    while 'token' not in token_holder and 'error' not in token_holder:
        httpd.handle_request()

    if 'token' in token_holder:
        print(f'\nSUCCESS\nToken: {token_holder["token"]}')
        print('Saved to .env')
        sys.exit(0)
    else:
        print(f'\nERROR: {token_holder["error"]}')
        sys.exit(1)
