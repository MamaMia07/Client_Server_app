import socket
import time, datetime
import json
import pathlib, hashlib

from  basic_methods import BasicMethods as bm

import account 

class ClntServCommunication():
    def __init__(self):
        pass

#DOSTOSOWAC DO USERA I ADMINA wraz z class Response    
    def logged_clnt_serv_communic(self, clnt_socket, addr):
##        with clnt_conn_socket:
##            print(f"Connected with {address[0]}")
            while True:
                data = clnt_socket.recv(1024).decode("utf-8")
                print(data)
                response = resp.prep_serv_response(data)
                print(response)
                clnt_conn_socket.sendall(response.encode("utf-8"))
                if data == "stop":
                    print("Connection terminated")
                    break


    def new_account(self):
        pass
    def sign_in(self):
        pass
    def log_out(self):
        pass
                
    def client_connection(self, clnt_socket, addr):
        with clnt_socket:
            print(f"Connected with {addr[0]}")
            
            welcome = {"Welcome to my tiny server! :)":"\nType"}
            start = {" sign:":"to sign in",
                    " new:": "to register",
                    " exit:": "to disconnect"}
            response =  {**welcome , **start}
            bm().send_serv_response(clnt_socket, response)
            while True:
                data = clnt_socket.recv(1024).decode("utf-8")
                if data not in ["sign", "new", "exit"]:
                    response = {"bad command:": data}
                    print(response)
                    bm().send_serv_response(clnt_socket, response)
               
                else: break
            print(data)
     #  menu wybor zawsze exit  !!!!!!!!!!!     
            if data == "new":
                client_registration = account.NewUserRegistration()
                client_registration.new_user_data_setting(clnt_socket,addr)


            if data == "sign":
                user_signin = account.SignInUser()
                user_signin.users_sign_in(clnt_socket,addr)
                print(user_signin.username)
                print(user_signin.status)
             # UTWORZ NOWEGO USER.

             
                #self.logged_clnt_serv_communic(clnt_socket, addr)
            elif data == "exit":
                print("Connection terminated") # DODAĆ ZAKOŃCZENIE thread
                #clnt_socket.close()  ?? nie dziala
            
                
            



        
