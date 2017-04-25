#!/usr/bin/python

import sys
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

ssl = {
    'certfile':  'tearbirds.crt',
    'keyfile': 'tearbirds.key',
    'ciphers': 'RSA',
}

def app(environ, start_response):
    if environ["PATH_INFO"] == '/echo':
        ws = environ["wsgi.websocket"]
        while True:
            src = ws.receive()
            if src is None:
                break
            ws.send(src)
    else:
        if environ["PATH_INFO"] == '/':
            path = "index.html"
        else:
            path = environ["PATH_INFO"][1:]
        f = open(path)
        content = f.read()
        f.close()

        start_response("200 OK", [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(content)))
                ])  
        return iter([content])

if __name__=="__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 8001), app, handler_class=WebSocketHandler, **ssl)
    server.serve_forever()
