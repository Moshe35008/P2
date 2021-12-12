import socket
import sys
import time
import os
import string
import random
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import stat

os.umask(000)

CHUNK_SIZE = 1_000_000
all_dict = {}  # the main dict


# def send_files(fold_path):
#     client_socket.send(str.encode(os.path.dirname(fold_path)))
#     for filename in os.listdir(fold_path):
#         f = os.path.join(fold_path, filename)
#         # checking if it is a file
#         if os.path.isfile(f):
#             with open(f, "rb") as to_read:
#                 while True:
#                     bytes_read = to_read.read(CHUNK_SIZE)
#                     if not bytes_read:
#                         break
#                     client_socket.send(str.encode(f))
#                     client_socket.send(bytes_read)
#         else:
#             send_files(os.path.abspath(f))

def id_generator(size=128, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory


def delete_dir_tree(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            os.remove(f)
        else:
            delete_dir_tree(f)
            os.remove(f)

    # project_path = os.path.dirname(sys.argv[0])
    # parent_dir_name = client_identifier
    # path = os.path.join(project_path, parent_dir_name)
    # os.mkdir(path)
    # dir_name = client_socket.recv(100).decode("utf-8")
    # path = os.path.join(path, dir_name)
    # os.mkdir(path)
    # while True:
    #     name = client_socket.recv(100).decode("utf-8")
    #     if '.' in name:
    #         f = open(name, 'a+')
    #         f.write(client_socket.recv(CHUNK_SIZE).decode("utf-8"))
    #     else:
    #         generate_dir_tree(name)


def send_files(fold_path):
    for filename in os.listdir(fold_path):
        after = "T3H4E5N"
        f = os.path.join(fold_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, "r") as to_read:
                to_read = to_read.read()
                client_socket.send(
                    (new_id + after + "1" + after + fold_path + after + filename + after + to_read).encode())
        else:
            # message = folder_id + after + message_type + after + path + after + the_new + after + detail
            client_socket.send(
                (new_id + after + "1" + after + fold_path + after + filename + after + "CREATEIT").encode())
            data = client_socket.recv(CHUNK_SIZE)
            send_files(os.path.join(fold_path, filename))


def generate_dir_tree(client_identifier, folder):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.mkdir(os.path.join(this_dir, client_identifier))
    os.mkdir(os.path.join(this_dir, client_identifier, folder))


def create_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if to_save:  # NOT SAVING FOR THE FIRST TIME!
            part_path = os.path.join(part_path, slash)
        if os.path.basename(folder_path) == slash:
            to_save = True
    full_path = os.path.join(folder_path, part_path, message[3])
    if message[4] == "CREATEIT":
        os.mkdir(full_path)
    else:
        with open(full_path, "w") as f:
            if message[4] != "N1o2n3e":
                f.write(message[4])
    client_socket.send("ok".encode())


def move_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if to_save:
            part_path = os.path.join(part_path, slash)
        if os.path.basename(folder_path) == slash:
            to_save = True
    old_path = os.path.join(folder_path, part_path, message[3])
    new_path = os.path.join(folder_path, part_path, message[4])
    os.rename(old_path, new_path)


def del_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if to_save:
            part_path = os.path.join(part_path, slash)
        if os.path.basename(folder_path) == slash:
            to_save = True
    full_path = os.path.join(folder_path, part_path, message[3])
    os.chmod(full_path, stat.S_IWRITE)
    for root, dirs, files in os.walk(full_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.remove(full_path)


def change_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if to_save:
            part_path = os.path.join(part_path, slash)
        if os.path.basename(folder_path) == slash:
            to_save = True
    full_path = os.path.join(folder_path, part_path, message[3])
    with open(full_path, "w") as f:
        if message[4] != "N1o2n3e":
            f.write(message[4])


if __name__ == "__main__":
    this_path = os.path.dirname(os.path.abspath(__file__))
    i = 2
    utf = "utf-8"
    curr_path = os.path.dirname(sys.argv[0])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(sys.argv[1])))
    # w = Watcher(curr_path, MyHandler())
    # w.run()
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        data = client_socket.recv(CHUNK_SIZE)
        # print(data.decode(utf))
        # if the client is new we give him a new id and add him to the main dict
        # and create a copy of his folder.
        if data.decode("utf-8") == "new_client":
            new_id = id_generator()
            client_socket.send(new_id.encode())
            data = client_socket.recv(CHUNK_SIZE)  # getting the name of the folder
            generate_dir_tree(new_id, data.decode(utf))
            all_dict[new_id] = {client_address[0]: []}
        # the client is committing changes in the folder, we add the in the
        # different computers of the client

        elif "A1N2D" in data.decode("utf-8") or "T3H4E5N" in data.decode("utf-8"):
            packets = data.decode("utf-8").split("^")[:-1]
            for packet in packets:
                if "A1N2D" in packet:
                    id_folder_path = os.path.join(this_path, packet.split("A1N2D")[0])
                    for folder in os.listdir(id_folder_path):
                        folder_path = os.path.join(id_folder_path, folder)
                    create_name(packet.split("A1N2D"))
                elif "T3H4E5N" in packet:
                    # for key, value in all_dict[packet.split("T3H4E5N")[0]].items():
                    #     if key != client_address[0]:
                    #         all_dict[packet.split("T3H4E5N")[0]][key].append(packet)
                    id_folder_path = os.path.join(this_path, packet.split("T3H4E5N")[0])
                    for folder in os.listdir(id_folder_path):
                        folder_path = os.path.join(id_folder_path, folder)
                    if packet.split("T3H4E5N")[1] == "1":
                        create_name(packet.split("T3H4E5N"))
                    if packet.split("T3H4E5N")[1] == "2":
                        move_name(packet.split("T3H4E5N"))
                    if packet.split("T3H4E5N")[1] == "3":
                        del_name(packet.split("T3H4E5N"))
                    if packet.split("T3H4E5N")[1] == "4":
                        change_name(packet.split("T3H4E5N"))

                    # adding the task to all computers of client
                   # all_dict[]
                    for key in all_dict.keys():
                        for key2 in all_dict[key].keys():
                            if not key2 == client_address[0]:
                                all_dict[key][key2].append(data)
        # the client already logged in from this computer
        # and is just re-connecting. sending him his actions to make.
        elif client_address[0] in all_dict[data.decode("utf-8")].keys():
            # checking if this computer has actions to make.
            client_socket.send(f"{len(all_dict[data.decode('utf-8')][client_address[0]])}".encode())
            if len(all_dict[data.decode("utf-8")][client_address[0]]) != 0:
                for action in all_dict[data.decode("utf-8")][client_address[0]]:
                    client_socket.send(action)
                    # removing the action from clients to do
                    all_dict[data.decode("utf-8")][client_address[0]].remove(action)
            else:
                send_files(os.path.join(curr_path, data.decode("utf-8")))
        # the client already connected but is connecting from another new computer.
        else:
            pass
            # new_id = data.decode(utf)
            # all_dict[new_id] = {client_address[0]: []}
            # send_files(os.path.dirname(os.path.abspath(__file__)))
            # os.path.join(curr_path, data.decode("utf-8"))
        client_socket.close()
