#!/usr/bin/python3

import io
import logging
import socketserver
from threading import Condition
from http import server

page_index="""\
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 2px dotted red;
}
</style>
</head>
<body>

<h2>Bordered Table</h2>
<p>Use the CSS border property to add a border to the table.</p>

<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th> 
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
  <tr>
    <td>John</td>
    <td>Doe</td>
    <td>80</td>
  </tr>
</table>

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