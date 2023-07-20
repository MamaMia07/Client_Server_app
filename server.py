import socket
import time, datetime
import json
import threading
import hashlib

class ServInit():
    version = '0.1.0'
    HOST = "127.0.0.1"  
    PORT = 9090  
    def __init__(self):
        self.start = time.time()

        
class Response():
    def __init__(self, start_serv, version):
        self.help = {"stop": " : disconnect",
                        "info": " : server software version",
                        "uptime": " : server uptime",
                        "help": " : menu help"}
        self.start = start_serv
        self.version = version

    def set_serv_response(self, cmd):
        self.server_life = time.time() - self.start
        self.responses = {"info": {"server v.:": self.version},
                         "uptime": {"server uptime:": f"{self.server_life:.4f}s"},
                         "stop" : {"connection status:": "terminated"},
                         "help": self.help}
        if cmd in self.responses:
            return self.responses[cmd]
        else:
            return {"Unknown command.\nType 'help' for command list.":""}
 
    def prep_serv_response(self, cmd):
        self.serv_resp = self.set_serv_response(cmd)
        return json.dumps(self.serv_resp, indent = 4)

# DLA USERA- OPCJA ZMIANY HASLA


class NewAccount():
    def __init__(self):
        self.status = "user"
        self.username = ""
        self.password = ""
        self.name = ""
        self.date = ""

    def get_users_list(self):
        with open("admin/users.json", "r") as users_file:
            data = users_file.read()
        self.users_lst = json.loads(data)
        return self.users_lst


    def create_account(self):
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.account = {self.username :
                  { "status" :  self.status,
                   "username" : self.username,
                   "password" :  self.password,
                   "name" : self.name,
                   "creation date" : self.date}
                  }

    def save_new_account(self):
        self.users_lst.update(self.account)
        with open("admin/users.json", "w") as users_file:
            users_file.write(self.users_lst)

    def get_name(self, cmd):
        while True:
            self.name = cmd
            if self.name == "" :
                return {f"name {self.name}": "can not be empty"}
            else:
                return {f"name:{self.name}": "saved"}
                break

##    def get_name(self):
##        while True:
##            self.name = (input("name: "))
##            if self.name == "" :
##                return {f"name {self.name}": "can not be empty"}
##            else: break
##        return {f"name:{self.name}": "saved"}


    def get_username(self):
        forbidden_symb = """`~!@#$%^&*() +={[}}|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        while True:
            self.username = (input("username: ")).strip().lower()
            if self.username in self.users_lst:
                return {f"username {self.username}": "already exists"}
            elif self.username == "" :
                return {f"username {self.username}": "can not be empty"}
            elif any(symbol in forbidden for symbol in username):
                return {f"username {self.username} contains invalid char": f"{forbidden}"}
            else: break
        return {f"username {self.username}": "accepted"}


    def get_password(self):
        while True:
            pass1 = (input("password: "))
            pass2 = (input("repeat password: "))
            if pass1 != pass2:
                return {"different passwords have been entered":""}
            else: break
        code = hashlib.sha256()
        code.update(pass1.encode())
        self.password = code.hexdigest()
        return {"password": "saved"}


                



    





class ClientConnection():
    def __init__(self):
        pass

    def clnt_login(self, clnt_socket):
        welcome = "Welcome to my tiny server! :)\ntype: 'login' to log in\nor 'new' to create new account"
        clnt_conn_socket.sendall(welcome.encode("utf-8"))
        while True:
            data = clnt_conn_socket.recv(1024).decode("utf-8")
            if data not in ["login", "new"]:
                response = {"bad command :": data}
                print(response)
                response= json.dumps(response, indent = 4)
                clnt_conn_socket.sendall(response.encode("utf-8"))
            else: break
        if data == "new":
            response = {"Creating new account" : "\nname:"}
            response= json.dumps(response, indent = 4)
            clnt_conn_socket.sendall(response.encode("utf-8"))
            
##            response = {"name :": ""}
##            response= json.dumps(response, indent = 4)
##            clnt_conn_socket.sendall(response.encode("utf-8"))

            new_account = NewAccount()
            data = clnt_conn_socket.recv(1024).decode("utf-8")
            print(data)
            response = new_account.get_name(data)
            response= json.dumps(response, indent = 4)
            clnt_conn_socket.sendall(response.encode("utf-8"))
            print(f"account name {new_account.name}")





    def clnt_serv_communication(self, clnt_socket, addr):
        with clnt_conn_socket:
            print(f"Connected with {address[0]}")
            while True:
                data = clnt_conn_socket.recv(1024).decode("utf-8")
                print(data)
                response = resp.prep_serv_response(data)
                print(response)
                clnt_conn_socket.sendall(response.encode("utf-8"))
                if data == "stop":
                    print("Connection terminated")
                    break

    def client_connection(self, clnt_socket, addr):
       self.clnt_login(clnt_socket)
       self.clnt_serv_communication(clnt_socket, addr)





serv_init = ServInit()
resp = Response(serv_init.start, serv_init.version)
clnt = ClientConnection()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((serv_init.HOST, serv_init.PORT))
    server.listen()
    print("Listening...")
    threads = []
    while True:
        clnt_conn_socket, address = server.accept()
        t = threading.Thread(target = clnt.client_connection, args =(clnt_conn_socket, address))
        n = len(threads)
        threads.append(t)
        threads[n].start()

        if len(threads) == 0:
            print("Connection terminated")
            break
