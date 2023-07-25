import socket
import time, datetime
import json
import pathlib, hashlib
from  basic_methods import BasicMethods as bm


class Account():
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
                       "creation date" : self.date}}
        return account

    def set_name(self, cmd):
        self.name = cmd

    def set_username(self, cmd):
        self.username = cmd

    def set_password(self, cmd):
        code = hashlib.sha256()
        code.update(cmd.encode())
        self.password = code.hexdigest()
        



class NewUserRegistration():
    def __init__(self):
        self.new_account = Account()

    def insert_name(self,clnt_socket):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data == "" :
                response = {f"name {self.name}": "can not be empty"}
                bm().send_serv_response(clnt_socket, response)
            else:
                break
        return data
    
    def insert_username(self,clnt_socket):
        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        users_list = bm().read_from_file("admin/users.json")
        print(users_list)
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            data = data.lower().strip()
                   
            if data in users_list : 
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
            else: break
        return data


    def insert_password(self, clnt_socket):
        response = {"password:":""} 
        bm().send_serv_response(clnt_socket, response)
        while True:
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
            else: break
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


    def save_new_account(self):
        users_list = bm().read_from_file("admin/users.json")
        new_acc = self.new_account.create_account()
        users_list.update(new_acc)
        bm().save_file("admin/users.json", users_list)


    def new_user_data_setting(self, clnt_socket, addr):
        while True:
            response = {"Creating new account":"\nenter your name:"} 
            bm().send_serv_response(clnt_socket, response)

            accepted_name = self.insert_name(clnt_socket)
            self.new_account.set_name(accepted_name)
            print(f"zapisane imie użytkownika: {self.new_account.name}")

            response= {"username:":""}
            bm().send_serv_response(clnt_socket, response)
            
            accepted_username = self.insert_username(clnt_socket)
            self.new_account.set_username(accepted_username)
            print(f"zapisana nazwa użytkownika: {self.new_account.username}")

            accepted_pass = self.insert_password(clnt_socket)
            self.new_account.set_password(accepted_pass)
            print(f"zapisane haslo użytkownika: {self.new_account.password}")

            confirmation = self.confirm_account(clnt_socket)
            print(confirmation)
            if confirmation:
                self.save_new_account()
                bm().create_users_dir(self.new_account.username)
                response = {f"account for {self.new_account.username} created.\n":"\nType",
                            " sign:": "to sing in",
                            " exit:" : "to disconnect"}
                bm().send_serv_response(clnt_socket, response)
                break
        

class SignInUser():
    def __init__(self):
        self.users_list = bm().read_from_file("admin/users.json")
    
    def check_user(self, name):
        return name  in self.users_list
 
    def check_password(self, name, passw):
        return passw ==  self.users_list[name]["password"]
           
     def users_sign_in(self, clnt_socket):
        while True:
            response = {"username:":""} 
            bm().send_serv_response(clnt_socket, response)
            username = clnt_socket.recv(1024).decode("utf-8")

            response = {"password:":""} 
            bm().send_serv_response(clnt_socket, response)
            password = clnt_socket.recv(1024).decode("utf-8")

            if self.check_user(username) and self.check_password(username, password):
                status = self.user_list[username]["status"]
                logged_user = User(username, status)
                return logged_user
            break

            response = {f"account for {self.new_account.username} created.\n":"\nType",
                            " sign:": "to sing in",
                            " exit:" : "to disconnect"}
            bm().send_serv_response(clnt_socket, response)

        




        
    
        
