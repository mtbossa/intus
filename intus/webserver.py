"""
Responsible for creating and
managing the local server.
"""
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from intus import config


class Handler(BaseHTTPRequestHandler):
    """ Handles the requests from Javascript."""
    def do_OPTIONS(self):
        """Handle OPTIONS request."""
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTION')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, If-Modified-Since")
        self.end_headers()

    def do_GET(self):
        """Handle GET request."""
        last_modified_date = os.path.getmtime(config.get_showcase_json_file_path())
        last_modified_string = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_modified_date))

        request_last_modified_string = str(self.headers.get('If-Modified-Since'))

        if request_last_modified_string != last_modified_string:
            self.send_response(200)

            with open(config.get_showcase_json_file_path(), 'r') as f:
                posts = f.read()

            response = posts.encode()
        else:
            self.send_response(302, 'Not Modified')

            response = bytes('not modified', 'utf-8')

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTION')
        self.send_header('Content-Type', 'application/json')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, If-Modified-Since")
        self.send_header('Last-Modified', last_modified_string)
        self.end_headers()

        self.wfile.write(response)


def run_server() -> None:
    """Run the server."""
    PORT = 8000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, Handler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
