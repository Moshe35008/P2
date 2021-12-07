import socket
import sys
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

CHUNK_SIZE = 1_000_000


# dada
class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.directory = "C:\\Users\\User\\PycharmProjects\\network2\\CORPUS"
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
    ignore_modi = 0

    def on_created(self, event):
        message = ""
        path = ""
        after = "A1N2D_T3H4E5N"
        message_type = "1"
        full_path = event.src_path
        slashes = full_path.split('\\')
        the_new = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        detail = ""
        os.chmod(path, mode=0o777)
        if os.path.isfile(full_path):
            # detail = os.open(full_path, flags=os.O_RDONLY)
            with open(full_path, "r") as f:
                detail = f.read()
        else:
            detail = "N1o2n3e"
        message = message_type + after + path + after + the_new + after + detail
        print(message.split(after))
        self.ignore_modi = 2

    def on_moved(self, event):
        message = ""
        path = ""
        after = "A1N2D_T3H4E5N"
        message_type = "2"
        full_path = event.src_path
        slashes = full_path.split('\\')
        old_name = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        new_name = (event.dest_path).split('\\')[-1]
        message = message_type + after + path + after + old_name + after + new_name
        print(message.split(after))
        self.ignore_modi = 2

    def on_deleted(self, event):
        message = ""
        path = ""
        after = "A1N2D_T3H4E5N"
        message_type = "3"
        full_path = event.src_path
        slashes = full_path.split('\\')
        old_name = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        message = message_type + after + path + after + old_name
        print(message.split(after))
        self.ignore_modi = 2

    def on_modified(self, event):
        if self.ignore_modi:
            self.ignore_modi -= 1
            return
        else:
            message = ""
            path = ""
            after = "A1N2D_T3H4E5N"
            message_type = "4"
            full_path = event.src_path
            slashes = full_path.split('\\')
            the_new = (slashes[-1])
            slashes.remove(slashes[-1])
            for slash in slashes:
                path = path + slash + "\\"
            detail = ""
            os.chmod(path, mode=0o777)
            if os.path.isfile(full_path):
                # detail = os.open(path, flags=os.O_RDONLY)
                with open(full_path, "r") as f:
                    detail = f.read()
            else:
                detail = "N1o2n3e"
            message = message_type + after + path + after + the_new + after + detail
            print(message.split(after))


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
    s.send(str.encode(os.path.basename(fold_path)))
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
    # w = Watcher(curr_path, MyHandler())
    # w.run()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, int(server_port)))
    if is_new == 0:
        s.send(folder_id.encode())
    else:
        s.send(b'new_client')
        folder_id = s.recv(128)
        send_files(folder_path)
    s.close()
    # send_files(folder_path)
