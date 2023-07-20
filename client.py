import socket
import json

HOST = "127.0.0.1"  
PORT = 9090 
size = 1024

connected = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clnt_socket:
    clnt_socket.connect((HOST, PORT))
    print(clnt_socket.recv(size).decode("utf-8"))
    while connected: #True:
        request = input("")
        if request != "":
            clnt_socket.send(request.encode("utf-8"))
        else: continue
        data = ""
        while True:
            rec = clnt_socket.recv(size)
            data += rec.decode("utf-8")
            if len(rec) < size: break 
        if request == "stop": connected = False #break 

        for key in json.loads(data):
            print(f"{key} {json.loads(data)[key]}")
            

