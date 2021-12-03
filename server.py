import socket
import sys
import time
import os
import string
import random
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

CHUNK_SIZE = 1_000_000
#dad

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

    def on_created(self, event):
        print("added")

    def on_moved(self, event):
        print("moved")

    def on_deleted(self, event):
        print("deleted")  # Your code here

    def on_modified(self, event):
        pass


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


def send_files(fold_path):
    client_socket.send(str.encode(os.path.dirname(fold_path)))
    for filename in os.listdir(fold_path):
        f = os.path.join(fold_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, "rb") as to_read:
                while True:
                    bytes_read = to_read.read(CHUNK_SIZE)
                    if not bytes_read:
                        break
                    client_socket.send(str.encode(f))
                    client_socket.send(bytes_read)
        else:
            send_files(os.path.abspath(f))


if __name__ == "__main__":
    curr_path = os.path.dirname(sys.argv[0])
    w = Watcher(curr_path, MyHandler())
    w.run()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', sys.argv[1]))
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)
        data = client_socket.recv(128)
        if data.decode("utf-8") == "new_client":
            new_id = id_generator()
            client_socket.send(new_id.encode())
            generate_dir_tree(new_id)
        else:
            send_files(os.path.join(curr_path, data.decode("utf-8")))

        print('Received: ', data)
        client_socket.send(data.upper())
        data = client_socket.recv(100)
        print('Received: ', data)
        client_socket.send(data.upper())
        client_socket.close()
        print('Client disconnected')
