import socket
import json
import getpass

class Client():
    HOST = "127.0.0.1"  
    PORT = 9090 
    def __init__(self):
        self.size = 1024

##    def receive(self, clntsock):
##        data = ""
##        while True:
##            rec = clntsock.recv(client.size)
##            data += rec.decode("utf-8")
##            if len(rec) < self.size: break 
##        for key in json.loads(data):
##            print(f"{key} {json.loads(data)[key]}")
##        return data
##
##        
##    def send(self, clntsock, conn, data):
##        if "password" in data:
##             request = getpass.getpass(prompt = "> ")
##        else:
##            request = input("> ")
##        if request != "":
##            clntsock.send(request.encode("utf-8"))
##        #else: continue
##        if request == "exit": conn = False #break
    def receive(self, clntsock):
        data = ""
        while True:
            rec = clntsock.recv(client.size)
            data += rec.decode("utf-8")
            if len(rec) < self.size: break 
        for key in json.loads(data):
            print(f"{key} {json.loads(data)[key]}")
        return data
            
        
    def send(self, clntsock, conn, data):
        if "password" in data:
             request = getpass.getpass(prompt = "> ")
        else:
            while True:
                request = input("> ")
                if request != "":
                    clntsock.send(request.encode("utf-8"))
                    break

            if request == "exit": conn = False #break
    

client = Client()

connected = True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clnt_socket:
    clnt_socket.connect((client.HOST, client.PORT))

##    receive_thread = threading.Thread(target = client.receive,args =clnt_socket)
##    client.send(clnt_socket, connected, data)
    #send_thread = threading.Thread(target = client.send, args = clnt_socket)

##    data = client.receive(clnt_socket)
##    while connected:
##        client.send(clnt_socket, connected, data)
##        try:
##            data = client.receive(clnt_socket)
##        except: pass



    # thread dla nasłuchiwania i wysyłania


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
       
        

       

