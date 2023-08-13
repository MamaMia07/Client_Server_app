import socket, threading, json
import time
import account
#from clnt_server_com import ClntServCommunication
from clnt_server_com import Server


class ServInit():
    version = '0.1.0'
    HOST = "127.0.0.1"  
    PORT = 9090  
    def __init__(self):
        self.start = time.time()


serv_init = ServInit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((serv_init.HOST, serv_init.PORT))
    server.listen()
    print("Listening...")

    users =[] 
    threads = []
    while True:
        clnt_conn_socket, address = server.accept()
        clnt_serv = Server(serv_init.start, serv_init.version)
        users.append(clnt_conn_socket)
        #print(len(users)) 
        thread = threading.Thread(target = clnt_serv.handle_client, args =(clnt_conn_socket, address))
        n = len(threads)
        threads.append(thread)
        threads[n].start()

        
        
