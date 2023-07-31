import datetime
from  tools import BasicMethods as bm


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
        self.password = bm().code_password(cmd)



class NewUserRegistration():
    def __init__(self):
        self.new_account = Account()

    def insert_name(self,clnt_socket):
        while True:
            recvd_name = clnt_socket.recv(1024).decode("utf-8")
            if recvd_name == "" :
                response = {f"name ": "can not be empty"}
                bm().send_serv_response(clnt_socket, response)
            else: break
        return recvd_name
    
    def insert_username(self,clnt_socket):
        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        users_list = bm().read_from_file("admin/users.json")
        while True:
            recvd_usernm = clnt_socket.recv(1024).decode("utf-8")
            recvd_usernm = recvd_usernm.lower().strip()
            if recvd_usernm in users_list : 
                response = {f"username {recvd_usernm}": "already exists\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            elif recvd_usernm == "" :
                response = {f"username ": "can not be empty\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            elif any(symbol in forbidden for symbol in recvd_usernm):
                response = {f"username {recvd_usernm} contains invalid char": f"{forbidden}\nusername:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            else: break
        return recvd_usernm

    def insert_password(self, clnt_socket):
        response = {"password:":""} 
        bm().send_serv_response(clnt_socket, response)
        while True:
            pass1 = clnt_socket.recv(1024).decode("utf-8")
            if len(pass1) < 4:
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

    def new_user_data_setting(self, clnt_socket, menu):
        response = {"Creating new account":"\nenter your name:"} 
        bm().send_serv_response(clnt_socket, response)

        accepted_name = self.insert_name(clnt_socket)
        self.new_account.set_name(accepted_name)

        response= {"username:":""}
        bm().send_serv_response(clnt_socket, response)
        
        accepted_username = self.insert_username(clnt_socket)
        self.new_account.set_username(accepted_username)

        accepted_pass = self.insert_password(clnt_socket)
        self.new_account.set_password(accepted_pass)

        confirmation = self.confirm_account(clnt_socket)
        if confirmation:
            self.save_new_account()
            bm().create_users_dir(self.new_account.username)
            response = {f"Account for {self.new_account.username} created.":"\n"}
            response.update(menu)
        else:
            response = {f"New account not approved.":"\n"}
            response.update(menu)
        bm().send_serv_response(clnt_socket, response)



class SignInUser():
    def __init__(self): 
        self.username = ""
        self.status = ""

    def check_user(self, name):
        users_list = bm().read_from_file("admin/users.json")
        return name  in users_list
 
    def check_password(self, name, passw):
        users_list = bm().read_from_file("admin/users.json")
        try:
            find_pass = users_list[name]["password"]
        except: return False
        return passw == users_list[name]["password"]

    def sign_in_user(self, clnt_socket, start_menu, user_menu, adm_menu):
        users_list = bm().read_from_file("admin/users.json")
        response = {"username:":""} 
        bm().send_serv_response(clnt_socket, response)
        recvd_username = clnt_socket.recv(1024).decode("utf-8")

        response = {"password:":""} 
        bm().send_serv_response(clnt_socket, response)
        recvd_password = clnt_socket.recv(1024).decode("utf-8")
        recvd_password = bm().code_password(recvd_password)

        if self.check_user(recvd_username) and self.check_password(recvd_username, recvd_password):
            self.username = recvd_username
            self.status = users_list[recvd_username]["status"]
            username = recvd_username
            status = users_list[recvd_username]["status"]
            response = {f"User {self.username}":"is logged in\n"}
            if status == "admin" : user_menu.update(adm_menu)
            response.update(user_menu)
        else:
            response = {f"Username or passwrd incorrect.":"\n"}
            response.update(start_menu)
        bm().send_serv_response(clnt_socket, response)
