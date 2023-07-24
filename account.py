import socket
import time, datetime
import json
import hashlib

from  basic_methods import BasicMethods as bm

class NewAccount():
    def __init__(self):
        self.status = "user"
        self.username = ""
        self.password = ""
        self.name = ""
        self.date = "" 
        users_lst = bm().read_from_file("admin/users.json")

    def create_account(self):
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        account = {self.username :
                      { "status" :  self.status,
                       "username" : self.username,
                       "password" :  self.password,
                       "name" : self.name,
                       "creation date" : self.date}
                   }

        #print(account)         
        return account

    
##    def update_users_lst(self):
##        #self.account = self.create_account()
##        return self.users_lst.update(self.account)

##    def save_new_account(self):
##        users_lst = self.update_users_lst()
##        with open("admin/users.json", "w") as users_file:
##            users_file.write(users_lst)

    def set_name(self, cmd):
        self.name = cmd

    def set_username(self, cmd):
        self.username = cmd

    def set_password(self, cmd):
        code = hashlib.sha256()
        code.update(cmd.encode())
        self.password = code.hexdigest()
        

##    def create_save_new_account(self):
##        self.account = self.create_account()
##        users_lst.update(self.account)
##        #self.update_users_lst()
##        self.save_new_account()
##
##    def prt(self):
##        cc = self.create_account()
##        print(vars(self.cc))

#new user registration
#class ClientConnection():
class NewUserRegistration():
    def __init__(self):
        self.users_list = bm().read_from_file("admin/users.json")

    def insert_name(self,clnt_socket):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data == "" :
                response = {f"name {self.name}": "can not be empty"}
                bm().send_serv_response(clnt_socket, response)
            else:
##                response = {f"name:{self.name}": "saved"}
##                self.send_serv_response(clnt_socket, response)
                break
        return data
        
    
    def insert_username(self,clnt_socket):
        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            data = data.lower().strip()
                   
            if data in self.users_list :#["ola", "admin"]:
                response = {f"username {data}": "already exists\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            elif data == "" :
                response = {f"username {data}": "can not be empty\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            elif any(symbol in forbidden for symbol in data):
                response = {f"username {data} contains invalid char": f"{forbidden}\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            else:
                #new_account.get_username(data)
                #response ={f"username {data}": "accepted"}
                #self.send_serv_response(response)
                break
        return data


    def insert_password(self, clnt_socket):
        response = {"password:":""} 
        bm().send_serv_response(clnt_socket, response)
        while True:
##            response = {"password:":""} 
##            self.send_serv_response(response)
            pass1 = clnt_socket.recv(1024).decode("utf-8")

            if len(pass1)<4:
                response = {"password should have at least":"4 characters\npassword:"}
                bm().send_serv_response(clnt_socket, response)
                continue

            response = {"repeat password:":""}
            bm().send_serv_response(clnt_socket, response)
            pass2 = clnt_socket.recv(1024).decode("utf-8")

            if pass1 != pass2:
                response = {"two different passwords have been entered":"\npassword:"}
                bm().send_serv_response(clnt_socket, response)
                continue
                    
            else:
                #response = {"password saved":""}
                #ClientConnection().send_serv_response(clnt_socket, response)
                break
        return pass1
        

    def confirm_account(self, clnt_socket):
        confirm = True
        while True:
            response = {"confirm the entered data":"y/n ?"} 
            bm().send_serv_response(clnt_socket, response)
            confirmation = clnt_socket.recv(1024).decode("utf-8")
            if confirmation  in ["y", "n"]:
                break
            else: continue
        if confirmation == "n": confirm = False
        return confirm


    def save_new_account(self, userslst ):
        new_acc = new_account.create_account()
        userslist.update(new_acc)
        bm().save_file("admin/users.json",self.userslist)


    def new_user_details_set(self, clnt_socket, addr):
        new_account = NewAccount()
        while True:
            response = {"Creating new account":"\nenter your name:"} #,"name:" : ""}
            bm().send_serv_response(clnt_socket, response)

            accepted_name = self.insert_name(clnt_socket)
            new_account.set_name(accepted_name)
            print(f"zapisane imie użytkownika: {new_account.name}")

            response= {"username:":""}
            bm().send_serv_response(clnt_socket, response)
            
            accepted_username = self.insert_username(clnt_socket)
            new_account.set_username(accepted_username)
            print(f"zapisana nazwa użytkownika: {new_account.username}")

            accepted_pass = self.insert_password(clnt_socket)
            new_account.set_password(accepted_pass)
            print(f"zapisane haslo użytkownika: {new_account.password}")

            confirmation = self.confirm_account(clnt_socket)
            if confirmation:
            #new_account.create_save_new_account()
            #new_account.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                self.save_new_account(self.users_list)
                print(self.users_list)
                #print(vars(new_account))
##                print(new_account.name)
##                print(new_account.username)
##                print(new_account.password)
##                print(new_account.status)
##                print(new_account.date)
##                print(new_account.users_lst)
##                print("")
##                print(acc)
##                print("")
##                print(new_account.account)
                break
        

        
        
    
        





class ClientConnection():
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

                
    def client_connection(self, clnt_socket, addr):
        self.client_registration = NewUserRegistration()
        with clnt_socket:
            print(f"Connected with {addr[0]}")
            response = {"Welcome to my tiny server! :)":"\ntype:",
                    "login:":" to log in",
                    "new:": "to create new account",
                    "exit:": "to disconnect"}
            bm().send_serv_response(clnt_socket, response)
            while True:
                data = clnt_socket.recv(1024).decode("utf-8")
                if data not in ["login", "new", "exit"]:
                    response = {"bad command:": data}
                    print(response)
                    bm().send_serv_response(clnt_socket, response)
               
                else: break
            print(data)

            try:
                if data == "new":
                    #new_account = NewAccount()
                #self.new_user_details(clnt_socket,addr)
                    self.client_registration.new_user_details_set(clnt_socket,addr)
                    
                self.logged_clnt_serv_communic(clnt_socket, addr)
            except: clnt_socket.close()

