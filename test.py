import socket
import sys
import time
import watchdog
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import string
import random


class Watcher:

    def __init__(self, directory="."):
        self.observer = Observer()

        self.handler = PatternMatchingEventHandler("[*]")
        self.handler.on_moved = self.on_moved
        self.handler.on_deleted = self.on_deleted
        self.handler.on_created = self.on_created
        self.handler.on_modified = self.on_modified

        self.directory = directory

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")

    def on_created(self, event):
        print("added")

    def on_moved(self, event):
        print("moved")

    def on_deleted(self, event):
        print("deleted")  # Your code here

    def on_modified(self, event):
        pass


if __name__ == "__main__":
    w = Watcher("C:\\Users\\ariel\\Downloads\\P2-master\\P2-master\\CORPUS")
    w.run()
