import socket
import sys
import time
import watchdog
import os
CHUNK_SIZE = 1_000_000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.150.128', 12345))
s.send(b'Moshe Schnaps')
data = s.recv(100)
print("Server sent: ", data)
s.send(b'208493064')
data = s.recv(100)
print("Server sent: ", data)
s.close()


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
    send_files(folder_path)
