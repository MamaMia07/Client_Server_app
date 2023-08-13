import account 
import user
import json
from  tools import BasicMethods as bm


class ClntServCommunication():
    def __init__(self, start_serv, version):
        
        self.serv_info = {"info": " : server software version",
                          "uptime": " : server uptime"
                          }
        self.serv_start = start_serv
        self.version = version
        
        self.start_menu = {"\nType":"",
                      "sign":": sign in",
                      "new": ": register new account",
                      "exit": ": disconnect"}

        self.user_menu = {"\nType":"",
                      "new" : ": send new message",
                      "read":  ": read new messages in your mailbox",
                      "mailbox": ": read all messages in your mailbox",
                      "sent": ": read sent messages",
                      "exit": ": disconnect"}
        self.admin_menu = {"users": " : list of users",
                          "pass": " : change user's passwrd",
                           "delete": " : delete user's account"
                          }

        self.admin_menu = {**self.admin_menu, **self.serv_info}

    
    def send_serv_response(self, clnt_socket, resp):
        response= json.dumps(resp, indent = 4)
        clnt_socket.sendall(response.encode("utf-8"))

    def new_user_data_setting(self, clnt_socket):
        client_registration = account.NewUserRegistration()
        response = {"Creating new account":"\nenter your name:"} 
        self.send_serv_response(clnt_socket, response)
        while True:
            recvd_name = clnt_socket.recv(1024).decode("utf-8")
            response = client_registration.insert_name(recvd_name)
            if response == True:
                break
            else: self.send_serv_response(clnt_socket, response)

        while True:
            response= {"username:":""}
            self.send_serv_response(clnt_socket, response)
            recvd_username = clnt_socket.recv(1024).decode("utf-8")
            response = client_registration.insert_username(recvd_username)
            if response == True:
                break
            else: self.send_serv_response(clnt_socket, response)

        while True:
            response = {"password:":""} 
            self.send_serv_response(clnt_socket, response)
            recvd_pass1 = clnt_socket.recv(1024).decode("utf-8")
            response = {"repeat password:":""}
            self.send_serv_response(clnt_socket, response)
            recvd_pass2 = clnt_socket.recv(1024).decode("utf-8")
            response = client_registration.insert_password(recvd_pass1, recvd_pass2)
            if response == True:
                break
            else: self.send_serv_response(clnt_socket, response)

        while True:
            response = {"confirm the entered data":"y/n ?"} 
            self.send_serv_response(clnt_socket, response)
            recvd_confirm = clnt_socket.recv(1024).decode("utf-8")
            response = client_registration.confirm_account(recvd_confirm)
            if response != False:
                response.update(self.start_menu)
                self.send_serv_response(clnt_socket, response)
                break
        

    def get_username(self, clnt_socket, response = {"username:":""} ): 
        #response = {"username:":""} 
        self.send_serv_response(clnt_socket, response)
        recvd_username = clnt_socket.recv(1024).decode("utf-8")
        return recvd_username


    def get_password(self, clnt_socket, response = {"password:":""}): 
        #response = {"password:":""} 
        self.send_serv_response(clnt_socket, response)
        recvd_password = clnt_socket.recv(1024).decode("utf-8")
        recvd_password = bm().code_password(recvd_password)
        return recvd_password


    def set_logged_user_permissions(self, recvd_username, recvd_password):
        self.user_in = account.SignInUser()
        self.user_in.sign_in_user(recvd_username, recvd_password)
        if self.user_in.logged_in:
            response = {f"User {recvd_username}":"is logged in\n"}
            self.logged_in_user = self.user_in.logged_in_user()
            if self.user_in.status == "admin" :
                self.user_menu =  {**self.user_menu , **self.admin_menu}
            response.update(self.user_menu)
        else:
            response = {f"Username or passwrd incorrect.":"\n"}
            response.update(self.start_menu)
        return response

    def sign_in_user(self, clnt_socket):
        recvd_username = self.get_username(clnt_socket)
        recvd_password = self.get_password(clnt_socket)
        response = self.set_logged_user_permissions(recvd_username, recvd_password)
        self.send_serv_response(clnt_socket, response)

        
# ========== to do klasy Server=============
    def start_user_connection(self, clnt_socket, addr):
        print(f"Connected with {addr[0]}")
        welcome = {"Welcome to my tiny server! :)":""}
        response =  {**welcome , **self.start_menu}
        self.send_serv_response(clnt_socket, response)
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in  self.start_menu:
                response = {"bad command:": data}
                self.send_serv_response(clnt_socket, response)
                continue
            if data == "new":
               self.new_user_data_setting(clnt_socket)
            if data == "sign":
                self.sign_in_user(clnt_socket)
                if self.user_in.logged_in: 
                    break
            if data == "exit":
                print(f"Connection with {addr[0]} terminated")
                break

#=============logged user============================

    def read_messages(self, clnt_socket, messages):
        msg_nmb = 0
        for key in messages:
            response = messages[key]
            msg_nmb += 1
            if msg_nmb < len(messages):
                response.update({"\nnext message?": "y/n"})
                self.send_serv_response(clnt_socket, response)
                while True:
                    answ = clnt_socket.recv(1024).decode("utf-8")
                    if answ in[ "n", "y"]:
                        break
                    bm().send_serv_response(clnt_socket, response)
                if answ == "n":
                    self.send_serv_response(clnt_socket, self.user_menu)
                    break
            else:
                response.update(self.user_menu)
                self.send_serv_response(clnt_socket, response) 

    def read_new_msgs(self, clnt_socket):
        messages = self.logged_in_user.read_new_msgs()
        self.read_messages(clnt_socket, messages)

    def read_all_msgs(self, clnt_socket):
        messages = self.logged_in_user.read_old_msgs()
        self.read_messages(clnt_socket, messages)

    def read_sent_msgs(self, clnt_socket):
        messages = self.logged_in_user.read_sent_msgs()
        self.read_messages(clnt_socket, messages)

    def create_new_message(self, clnt_socket):
        new_msg = self.logged_in_user.send_msg()

        response = {"\nCreating new message":"\nenter the message recipier:"} 
        bm().send_serv_response(clnt_socket, response)
        while True:
            recvd_recipient = clnt_socket.recv(1024).decode("utf-8")
            response = new_msg.enter_recipient(recvd_recipient)
            if response == True:
                break
            bm().send_serv_response(clnt_socket, response)

        response= {"message content:":""}
        bm().send_serv_response(clnt_socket, response)
        while True:
            recvd_text = clnt_socket.recv(1024).decode("utf-8")
            response = new_msg.enter_msg_text(recvd_text)
            if response == True:
                break
            bm().send_serv_response(clnt_socket, response)
        response = {"Send the message?":"y/n ?"} 
        bm().send_serv_response(clnt_socket, response)
        while True:
            confirm = clnt_socket.recv(1024).decode("utf-8")
            if confirm  in ["y", "n"]:
                response = new_msg.send_new_msg(confirm)
                response.update(self.user_menu)
                bm().send_serv_response(clnt_socket, response)
                break


    def get_users_list(self, clnt_socket):
        response = self.logged_in_user.list_of_users()
        response.update(self.user_menu)
        bm().send_serv_response(clnt_socket, response)


    def change_users_password(self, clnt_socket):
        response = {"Change user's passwrd:":"",
                "enter username:" : ""}
        recvd_username = self.get_username(clnt_socket, response)
##            bm().send_serv_response(clnt_socket, response)
##            recvd_user_account = clnt_socket.recv(1024).decode("utf-8")
        response = {"enter new user's password:":"\n"}
        recvd_new_pass = self.get_password(clnt_socket, response)

        response = self.logged_in_user.change_password(recvd_username, recvd_new_pass)
        response.update(self.user_menu)
        bm().send_serv_response(clnt_socket, response)

    def delete_users_account(self, clnt_socket):
        response = {"Deleting user's account:":"",
                "enter username:" : ""} 
        recvd_username = self.get_username(clnt_socket, response)
        response = self.logged_in_user.delete_account(recvd_username)
        response.update(self.user_menu)
        bm().send_serv_response(clnt_socket, response)
  
# +============ to do klasy Server==========
    def logged_user(self, clnt_socket, addr):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in self.user_menu: 
                response = {"bad command:": data}
                print(response)
                self.send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                self.create_new_message(clnt_socket)
            if data == "read":
                self.read_new_msgs(clnt_socket)
            if data == "mailbox":
                self.read_all_msgs(clnt_socket)
            if data == "sent":
                self.read_sent_msgs(clnt_socket)
            if data == "exit":
                print(f"Connection with {addr[0]} terminated")
                break

# POPRAWIC========================

   # admin permissions 
            if data in self.serv_info:
                response = self.logged_in_user.send_serv_info(data, self.serv_start,self.version)
                response.update(self.user_menu)
                bm().send_serv_response(clnt_socket, response)
                #self.logged_in_user.send_serv_info(clnt_socket, data, self.serv_start,self.version, self.user_menu)

            if data == "users":
                #self.logged_in_user.list_of_users(clnt_socket, self.user_menu)
                self.get_users_list(clnt_socket)

            if data == "pass":
                self.change_users_password(clnt_socket)
                #self.logged_in_user.change_password(clnt_socket, self.user_menu)

            if data == "delete":
                self.delete_users_account(clnt_socket)
                #self.logged_in_user.delete_account(clnt_socket, self.user_menu)

    def handle_client(self, clnt_socket, addr):
        with clnt_socket:
            self.start_user_connection(clnt_socket, addr)
            self.logged_user(clnt_socket, addr)
