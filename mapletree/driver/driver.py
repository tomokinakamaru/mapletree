# coding:utf-8

import os
import subprocess
import sys
from wsgiref.simple_server import make_server
from .watcher import Watcher


_STUB_PROCESS = '--wsgidriver-stub-process'


def run(app, host='localhost', port=5000):
    is_stub_process = (sys.argv[-1] == _STUB_PROCESS)
    abs_script_path = os.path.abspath(sys.argv[0])

    if is_stub_process:
        print(': starting stub process')

        httpd = make_server(host, port, app)
        on_change = lambda: httpd.shutdown()

        app_dir = os.path.dirname(abs_script_path)
        watcher = Watcher(app_dir, on_change)

        watcher.start()
        httpd.serve_forever()

    else:
        print(': starting driver process')

        stub_cmd = [sys.executable] + sys.argv + [_STUB_PROCESS]
        while True:
            try:
                if subprocess.call(stub_cmd) != 0:
                    break

            except KeyboardInterrupt:
                break
