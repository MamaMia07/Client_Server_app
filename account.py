import datetime
import user
import database as db


class Account():
    def __init__(self):
        self._username = ""
        self._password = ""
        self._name = ""
       
    def create_account(self):
        return db.save_new_account(self._username, self._password,  self._name)

    def set_name(self, cmd):
        self._name = cmd

    def set_username(self, cmd):
        self._username = cmd

    def set_password(self, cmd):
        self._password = cmd   



class NewUserRegistration():
    def __init__(self):
        self.new_account = Account()


    def insert_name(self,recvd_name):
        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        if recvd_name == "" :
            response = {f"name ": "can not be empty"}
        elif any(symbol in forbidden for symbol in recvd_name):
            response = {f"username {recvd_username} contains invalid char": "\nusername:"}
        else:
            self.new_account.set_name(recvd_name)
            response = True
        return response

    
    def insert_username(self,recvd_username):
        recvd_username = recvd_username.lower().strip()

        forbidden_symb = """`~!@#$%^&*() +={[}}]|\:;"'<,>?/"""
        forbidden = set(forbidden_symb)
        users_list = db.select_users()

        if any(user[0] == recvd_username for user in users_list):
            response = {f"username {recvd_username}": "already exists\nusername:"}
        elif recvd_username == "" :
            response = {f"username ": "can not be empty\nusername:"}
        elif any(symbol in forbidden for symbol in recvd_username):
            response = {f"username {recvd_username} contains invalid char": "\nusername:"}
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
                if self.new_account.create_account():
                    response = {f"Account for {self.new_account._username} created.":""}
                else:
                    response = {f"New account not approved.":"\n"}
        else:
            response =  False
        return response




class SignInUser():
    def __init__(self): 
        self.username = ""
        self.status = ""
        self.logged_in = False

    def sign_in_user(self, recvd_username, recvd_pswrd):
        recvd_username = recvd_username.lower().strip()
        passw = db.hash_pswrd(recvd_pswrd)

        user_data = db.user_log_data(recvd_username)
        if len(user_data)> 0:
            if user_data[0][0] == recvd_username and db.check_password(recvd_pswrd, user_data[0][1]):
                self.username = recvd_username
                self.status = user_data[0][2]
                self.logged_in = True
        return (self.logged_in, self.username, self.status)


    def logged_in_user(self):
        if self.status == "user":
            logged_in_user = user.User(self.username, self.status)
        elif self.status == "admin":
            logged_in_user = user.Admin(self.username, self.status)
        print(f"{self.username} logged in as {self.status}")
        db.set_login_date(self.username)
        return logged_in_user
