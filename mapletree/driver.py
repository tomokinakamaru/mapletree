# coding:utf-8

import os
import subprocess
import sys
import time
from wsgiref.simple_server import make_server
from threading import Thread


class Driver(object):
    STUB = '--mapletree-driver-stub'

    def __init__(self, app, port, target, interval):
        self.app = app
        self.port = port
        self.target = target
        self.interval = interval
        self.httpd = None

    def run_background(self):
        t = Thread(target=self._run_as_stub, args=(False, ))
        t.daemon = True
        t.start()

    def run(self):
        if self.STUB in sys.argv:
            self._run_as_stub()

        else:
            self._run_as_driver()

    def _run_as_driver(self):
        print(': starting driver')
        stub_cmd = [sys.executable] + sys.argv + [self.STUB]
        while True:
            try:
                if subprocess.call(stub_cmd) != 0:
                    break

            except KeyboardInterrupt:
                break

    def _run_as_stub(self, filewatch=True):
        print(': starting stub')

        self.httpd = make_server('localhost', self.port, self.app)

        if filewatch:
            filewatch_thread = Thread(target=self.watch_files)
            filewatch_thread.daemon = True
            filewatch_thread.start()

        self.httpd.serve_forever()

    def watch_files(self):
        keep_watching = True
        watch_start = time.time()

        while keep_watching:
            time.sleep(self.interval)

            for f in self.target_files():
                if watch_start < os.stat(f).st_mtime:
                    keep_watching = False
                    break

        print(': detected changes')
        self.httpd.shutdown()

    def target_files(self):
        for root, dirs, files in os.walk(self.target):
            for f in files:
                yield os.path.join(root, f)
