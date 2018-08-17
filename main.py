#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pwd
import socks
import socket
import time
import SocketServer
import logging
import daemonize
import tempfile

class BaseRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.cache = {}
        self.now = time.time()
        SocketServer.BaseRequestHandler.__init__(self, *args, **kwargs)

    def handle(self):
        if time.time() - self.now >= 60:
            self.cache.clear()
            self.now = time.time()
        request, connection = self.request
        if request[2:] in self.cache.keys():
            connection.sendto(request[0:2] + self.cache[request[2:]], self.client_address)
        else:
            forward = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            forward.set_proxy(socks.SOCKS5, os.environ.get('SOCKS_HOSTNAME') or 'localhost', int(os.environ.get('SOCKS_PORT') or '1080'), True)
            try:
                forward.sendto(request, (os.environ.get('DNS_HOSTNAME') or 'google-public-dns-a.google.com', int(os.environ.get('DNS_PORT') or '53')))
                response, server = forward.recvfrom(4096)
                connection.sendto(response, self.client_address)
                if len(response) > len(request):
                    self.cache[request[2:]] = response[2:]
            except:
                pass

def main():
    server = SocketServer.ThreadingUDPServer((os.environ.get('LISTEN_HOSTNAME') or 'localhost', int(os.environ.get('LISTEN_PORT') or '53')), BaseRequestHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    try:
        server.server_bind()
        os.setgroups([])
        os.setegid(pwd.getpwnam('nobody').pw_gid)
        os.seteuid(pwd.getpwnam('nobody').pw_uid)
        server.server_activate()
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

def daemon():
    pid = os.path.join(tempfile.gettempdir(), 'dns.pid')
    _daemon = daemonize.Daemonize(app='dns', pid=pid, logger=logging, action=main)
    if os.path.exists(pid):
        _daemon.exit()
    _daemon.start()

if __name__ == '__main__':
    if os.environ.get('PYTHON_ENV') == 'development':
        main()
    if os.environ.get('PYTHON_ENV') == 'production':
        daemon()
    if os.environ.get('PYTHON_ENV') is None:
        daemon()
