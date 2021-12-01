import socket
import sys
import time
import watchdog
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import string
import random

CHUNK_SIZE = 1_000_000

def id_generator(size=128, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
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


class MyHandler(FileSystemEventHandler):

    def on_any_event(self, event):
        print(event)  # Your code here


def delete_dir_tree(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            os.remove(f)
        else:
            delete_dir_tree(f)
            os.remove(f)


def generate_dir_tree(client_identifier):
    project_path = os.path.dirname(sys.argv[0])
    parent_dir_name = client_identifier
    path = os.path.join(project_path, parent_dir_name)
    os.mkdir(path)
    dir_name = client_socket.recv(100).decode("utf-8")
    path = os.path.join(path, dir_name)
    os.mkdir(path)
    while True:
        name = client_socket.recv(100).decode("utf-8")
        if '.' in name:
            f = open(name, 'a+')
            f.write(client_socket.recv(CHUNK_SIZE).decode("utf-8"))





if __name__ == "__main__":
    w = Watcher(".", MyHandler())
    w.run()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', sys.argv[1]))
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)
        data = client_socket.recv(100)
        print('Received: ', data)
        client_socket.send(data.upper())
        data = client_socket.recv(100)
        print('Received: ', data)
        client_socket.send(data.upper())
        client_socket.close()
        print('Client disconnected')
