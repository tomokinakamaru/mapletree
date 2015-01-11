# coding:utf-8

import os
import time
from threading import Thread


class Watcher(Thread):
    def __init__(self, target_dir, on_change):
        super(Watcher, self).__init__()
        self.daemon = True
        self.target_dir = target_dir
        self.on_change = on_change

    def run(self):
        mtimes = {}
        for f in self.watch_list():
            mtimes[f] = os.stat(f).st_mtime

        keep_watching = True
        while keep_watching:
            time.sleep(1)

            for f in self.watch_list():
                if f in mtimes:
                    if mtimes[f] < os.stat(f).st_mtime:
                        keep_watching = False
                        break

                else:
                    keep_watching = False
                    break

        print(': detected change')
        self.on_change()

    def watch_list(self):
        for root, dirs, files in os.walk(self.target_dir):
            for f in files:
                yield os.path.join(root, f)
