import json
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, If-Modified-Since")
        self.end_headers()

    def do_GET(self):
        last_modified = os.path.getmtime('local_data.json')
        last_modified_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_modified))

        request_last_modified = str(self.headers.get('If-Modified-Since'))

        if request_last_modified != last_modified_date:
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json')
            self.send_header('Last-Modified', str(last_modified_date))
            self.end_headers()
            with open('local_data.json', 'r') as f:
                posts = f.read()
            self.wfile.write(posts.encode())
        else:
            self.send_response(302, 'Not Modified')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.send_header('Last-Modified', str(last_modified_date))
            self.end_headers()
            self.wfile.write(bytes('not modified', 'utf-8'))


def run_server():
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, Handler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
