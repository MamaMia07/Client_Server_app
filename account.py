import datetime
from  tools import BasicMethods as bm
import user


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

    def insert_name(self,recvd_name):
        if recvd_name == "" :
            response = {f"name ": "can not be empty"}
        else:
            self.new_account.set_name(recvd_name)
            response = True
        return response
    
    def insert_username(self,recvd_username):
        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        users_list = bm().read_from_file("admin/users.json")
        recvd_username = recvd_username.lower().strip()
        if recvd_username in users_list : 
            response = {f"username {recvd_username}": "already exists\nusername:"}
        elif recvd_username == "" :
            response = {f"username ": "can not be empty\nusername:"}
        elif any(symbol in forbidden for symbol in recvd_username):
            response = {f"username {recvd_usernm} contains invalid char": f"{forbidden}\nusername:"}
        else:
            response = True
            self.new_account.set_username(recvd_username)
        return response

    def insert_password(self, pass1, pass2):
        if len(pass1) < 4:
            response = {"password should have at least":"4 characters\npassword:"}
        elif pass1 != pass2:
            response = {"two different passwords have been entered":"\npassword:"}
        else:
            response = True
            self.new_account.set_password(pass1)
        return response

    def confirm_account(self,confirmation):
        if confirmation  in ["y", "n"]:
            if confirmation == "y":
                self.save_new_account()
                response = {f"Account for {self.new_account.username} created.":"\n"}
            else:
                response = {f"New account not approved.":"\n"}
        else:
            response =  False
        return response

    def save_new_account(self):
        users_list = bm().read_from_file("admin/users.json")
        new_acc = self.new_account.create_account()
        users_list.update(new_acc)
        bm().save_file("admin/users.json", users_list)
        bm().create_users_dir(self.new_account.username)



class SignInUser():
    def __init__(self): 
        self.username = ""
        self.status = ""
        self.logged_in = False

    def check_user(self, name):
        users_list = bm().read_from_file("admin/users.json")
        return name  in users_list
 
    def check_password(self, name, passw):
        users_list = bm().read_from_file("admin/users.json")
        try:
            find_pass = users_list[name]["password"]
        except: return False
        return passw == users_list[name]["password"]

    def sign_in_user(self, recvd_username, recvd_password):
        recvd_username = recvd_username.lower().strip()
        users_list = bm().read_from_file("admin/users.json")
        if self.check_user(recvd_username) and self.check_password(recvd_username, recvd_password):
            self.username = recvd_username
            self.status = users_list[recvd_username]["status"]
            self.logged_in = True
        return (self.logged_in, self.username, self.status)


    def logged_in_user(self):
        if self.status == "user":
            logged_in_user = user.User(self.username, self.status)
        elif self.status == "admin":
            logged_in_user = user.Admin(user_in.username, user_in.status)
        print(f"{self.username} logged in as {self.status}")
        return logged_in_user
