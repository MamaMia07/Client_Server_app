import socket
import json
import getpass

class Client():
    HOST = "127.0.0.1"  
    PORT = 9090 
    def __init__(self):
        self.size = 1024

    def receive(self, clntsock):
        data = ""
        while True:
            rec = clnt_socket.recv(self.size)
     #       if not rec:
     #           break
            data += rec.decode("utf-8")
            if len(rec) < self.size: break 
        for key in json.loads(data):
            print(f"{key} {json.loads(data)[key]}")
        return data
        for key, value in json.loads(data).items():
            print(f"{key} {value}")
        return data
            
    def query(self, clntsock, data):
        if "password" in data:
            query = getpass.getpass(prompt = "> ")
        else:
            query = input("> ")
        return query

    

client = Client()

connected = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clnt_socket:
    clnt_socket.connect((client.HOST, client.PORT))

    rec_srv = client.receive(clnt_socket)
    while connected:
        request = client.query(clnt_socket, rec_srv)
        if request != "":
            clnt_socket.send(request.encode("utf-8"))
        else: continue
        if request == "exit":
            connected = False
        try:
            rec_srv = client.receive(clnt_socket)
        except ConnectionError as e:
            print(f"Connection error: {e}")
            pass
        except Exception as e:
            print(f"Error: {e}")
            pass

       

