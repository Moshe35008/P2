import socket
import sys
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

CHUNK_SIZE = 1_000_000


#dada
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

    def on_created(self, event):
        print("added")

    def on_moved(self, event):
        print("moved")

    def on_deleted(self, event):
        print("deleted")  # Your code here

    def on_modified(self, event):
        pass


def generate_dir_tree(client_identifier):
    project_path = os.path.dirname(sys.argv[0])
    parent_dir_name = client_identifier
    path = os.path.join(project_path, parent_dir_name)
    os.mkdir(path)
    dir_name = s.recv(100).decode("utf-8")
    path = os.path.join(path, dir_name)
    os.mkdir(path)
    while True:
        name = s.recv(100).decode("utf-8")
        if '.' in name:
            f = open(name, 'a+')
            f.write(s.recv(CHUNK_SIZE).decode("utf-8"))


def send_files(fold_path):
    s.send(str.encode(os.path.dirname(fold_path)))
    for filename in os.listdir(fold_path):
        f = os.path.join(fold_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, "rb") as to_read:
                while True:
                    bytes_read = to_read.read(CHUNK_SIZE)
                    if not bytes_read:
                        break
                    s.send(str.encode(f))
                    s.send(bytes_read)
        else:
            send_files(os.path.abspath(f))


if "__name__==__main__":
    curr_path = os.path.dirname(sys.argv[0])
    is_new = 0
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    folder_path = sys.argv[3]
    server_time = sys.argv[4]
    folder_id = 0
    if len(sys.argv) < 6:
        is_new = 1
    else:
        folder_id = sys.argv[5]
    w = Watcher(curr_path, MyHandler())
    w.run()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, server_port))
    if is_new == 0:
        s.send(folder_id.encode())
    else:
        s.send(b'new_client')
        folder_id = s.recv(128)
        send_files(curr_path)

    s.send(b'208493064')
    data = s.recv(100)
    s.close()
    # send_files(folder_path)
