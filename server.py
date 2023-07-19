import socket
import time, datetime
import json
import threading


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




class Account():
    def __init__(self):
        self.username = ""
        self.status = "user"
        self.password = ""
        self.name = ""
        self.date = datetime.datetime.now()#time.localtime()
# dd/mm/YY H:M:S
#dt_string = self.date .strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

        self.users_lst = self.users_list()

    def users_list(self):
    # utworzyc odczytanie pliku z usersami json

        
    def get_username(self):
##        while True:
##            self.username = input("username: ")
            
        


    def clnt_login(self, clnt_socket):
        welcome = "Welcome to my server! :)\n type: 'log in' to log in\nor 'new' to create new account"
        #response = json.dumps({"zaloguj" : "", "załóż konto":""}, indent = 4)
        #clnt_conn_socket.sendall(response.encode("utf-8"))
        clnt_conn_socket.sendall(welcome.encode("utf-8"))




class ClientConnection():
    def __init__(self):
        pass

##    def clnt_login(self, clnt_socket):
##        welcome = "Welcome to my server! :)\n type: 'log in' to log in\nor 'new' to create new account"
##        #response = json.dumps({"zaloguj" : "", "załóż konto":""}, indent = 4)
##        #clnt_conn_socket.sendall(response.encode("utf-8"))
##        clnt_conn_socket.sendall(welcome.encode("utf-8"))
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
       #self.clnt_login(clnt_socket)
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
    ##    with clnt_conn_socket:
    ##        print(f"Connected with {address[0]}")
    ##        while True:
    ##            data = clnt_conn_socket.recv(1024).decode("utf-8")
    ##            response = resp.prep_serv_response(data)
    ##            clnt_conn_socket.sendall(response.encode("utf-8"))
    ##            if data == "stop":
    ##                print("Connection terminated")
    ##                break
    ##        t1 = threading.Thread(target = client_connection, args =(clnt_conn_socket, address))
    ##        t1.start()                          
        t = threading.Thread(target = clnt.client_connection, args =(clnt_conn_socket, address))
        n = len(threads)
        threads.append(t)
        threads[n].start()

        if len(threads) == 0:
            print("Connection terminated")
            break
