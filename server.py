import socket, threading, json
import time
import account



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
# if cmd = "exit" -__>  clnt_conn_socket.close()



serv_init = ServInit()
resp = Response(serv_init.start, serv_init.version)
clnt = account.ClntServCommunication()

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
