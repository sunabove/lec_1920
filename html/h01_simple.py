#!/usr/bin/python3

import io
import logging
import socketserver
from threading import Condition
from http import server

page_index="""\
<html>
<head>
<title>My First Html Page</title>
</head>
<body>
<p>Hello World!</p>
</body>
</html>
"""

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = page_index.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content) 
        else:
            self.send_error(404)
            self.end_headers()
        pass
    pass
pass

class WebServer(socketserver.ThreadingMixIn, server.HTTPServer, server.BaseHTTPRequestHandler):
    allow_reuse_address = True
    daemon_threads = True
pass

server = WebServer( ('', 80) , StreamingHandler)
server.serve_forever()