import socket
import json
import getpass

class Client():
    HOST = "127.0.0.1"  
    PORT = 9090 
    def __init__(self):
        self.size = 1024

##    def receive(self,clntsock):
##        data = ""
##        while True:
##            rec = clntsock.recv(self.size)
##            data += rec.decode("utf-8")
##            if len(rec) < self.size: break 
##        for key in json.loads(data):
##            print(f"{key} {json.loads(data)[key]}")
##
        
##    def send(self, clntsock, conn):
##        request = input("> ")
##        if request != "":
##            clntsock.send(request.encode("utf-8"))
##       
##            if request == "stop": conn = False #break

    

client = Client()

connected = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clnt_socket:
    clnt_socket.connect((client.HOST, client.PORT))


##    client.receive(clnt_socket)
##    while connected:
##        request = input("> ")
##        if request != "":
##            clnt_socket.send(request.encode("utf-8"))
##       
##            if request == "stop": conn = False #break
##        try:
##            client.receive(clnt_socket)
##        except: continue
##        
    data = ""
    while True:
        rec = clnt_socket.recv(client.size)
        data += rec.decode("utf-8")
        if len(rec) < client.size: break 
    for key in json.loads(data):
        print(f"{key} {json.loads(data)[key]}")

    while connected: #True:
        if "password" in data:
             request = getpass.getpass(prompt = "> ")
        else:
            request = input("> ")
        if request != "":
            clnt_socket.send(request.encode("utf-8"))
        else: continue
        if request == "exit": connected = False #break
        
        try:
           data = ""
           while True:
               rec = clnt_socket.recv(client.size)
               data += rec.decode("utf-8")
               if len(rec) < client.size: break 
           for key in json.loads(data):
               print(f"{key} {json.loads(data)[key]}")
        except: pass
       
        

       

