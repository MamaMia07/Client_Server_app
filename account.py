import datetime
import user
#from database import *
import database as db
import bcrypt  # usunac!

class Account():
    def __init__(self):
        #self.status = "user"
        self.username = ""
        self.password = ""
        self.name = ""
        #self.date = "" 
       
    def create_account(self):
        return db.save_new_account(self.username, self.password,  self.name)
        #self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
##        account = {self.username :
##                      { #"status" :  self.status,
##                       "username" : self.username,
##                       "password" :  self.password,
##                       "name" : self.name,
##                       #"creation date" : self.date
##                        }
##                   }
##        return account



## ____!!!!!!!  geter i seter spróbowac ??? ___________

    def set_name(self, cmd):
        self.name = cmd

    def set_username(self, cmd):
        self.username = cmd

    def set_password(self, cmd):
        self.password = cmd    #db.hash_pswrd(cmd)



class NewUserRegistration():
    def __init__(self):
        self.new_account = Account()

    # ujednolicic funkcje name i username - dekorator?
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
        #users_list = read_from_file("admin/users.json")
        users_list = db.select_users()

        if any(user[0] == recvd_username for user in users_list):
        #if recvd_username in users_list : 
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
                #self.save_new_account()???
                if self.new_account.create_account():
                    response = {f"Account for {self.new_account.username} created.":""}
                else:
                    response = {f"New account not approved.":"\n"}
        else:
            response =  False
        return response

### zastapic zapisem do bazy
##    def save_new_account(self):
##        users_list = read_from_file("admin/users.json")
##        new_acc = self.new_account.create_account()
##        users_list.update(new_acc)
##        save_file("admin/users.json", users_list)
##        create_users_dir(self.new_account.username)



class SignInUser():
    def __init__(self): 
        self.username = ""
        self.status = ""
        self.logged_in = False


##    def check_user(self, username, users_list):
##        return any(user[0] == username for user in users_list)
##
##
##    def check_password(self, username, pswrd):
##        passw = db.hash_pswrd(pswrd)
##        return pswrd == db.get_password(username)[0][0] 



#!!!!!!!!!!! czy działa jak złe dane wpisze??? !!!!!!!!!!!!!!!

    def sign_in_user(self, recvd_username, recvd_pswrd):
        recvd_username = recvd_username.lower().strip()
        passw = db.hash_pswrd(recvd_pswrd)

        user_data = db.user_log_data(recvd_username)
        
        if user_data[0][0] == recvd_username and db.check_password(recvd_pswrd, user_data[0][1]):
            self.username = recvd_username
            self.status = user_data[0][2]
            self.logged_in = True


##        if self.check_user(recvd_username, users_list) and self.check_password(recvd_username, recvd_pswrd):
##            for lst in users_list:
##                if recvd_username in lst:
##                    self.username = recvd_username
##                    self.status = lst[1]
##                    break
##            self.logged_in = True

        #if self.check_user(recvd_username, users_list) and self.check_password(recvd_username, recvd_pswrd):
            #self.username = recvd_username
            #self.status = users_list[recvd_username]["status"]
#            self.logged_in = True
        return (self.logged_in, self.username, self.status)


    def logged_in_user(self):
        if self.status == "user":
            logged_in_user = user.User(self.username, self.status)
        elif self.status == "admin":
            logged_in_user = user.Admin(self.username, self.status)
        print(f"{self.username} logged in as {self.status}")
        return logged_in_user
