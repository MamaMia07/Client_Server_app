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

        self.user_menu = {"Type":"",
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
        

    def get_username_and_pass(self, clnt_socket): 
        response = {"username:":""} 
        self.send_serv_response(clnt_socket, response)
        recvd_username = clnt_socket.recv(1024).decode("utf-8")

        response = {"password:":""} 
        self.send_serv_response(clnt_socket, response)
        recvd_password = clnt_socket.recv(1024).decode("utf-8")
        recvd_password = bm().code_password(recvd_password)
        return (recvd_username, recvd_password)

    def log_in_info(self, logged_in, username, status):
        if logged_in:
            response = {f"User {username}":"is logged in\n"}
            if status == "admin" :
                self.user_menu =  {**self.user_menu , **self.admin_menu}
            response.update(self.user_menu)
        else:
            response = {f"Username or passwrd incorrect.":"\n"}
            response.update(self.start_menu)
        return response



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
                recvd_username, recvd_password = self.get_username_and_pass(clnt_socket)

                user_in = account.SignInUser()
                user_in.sign_in_user(recvd_username, recvd_password)
                response = self.log_in_info(user_in.logged_in, user_in.username, user_in.status,)
                #sign_in = self.sign_in(clnt_socket, self.start_menu, self.user_menu, self.admin_menu)
                self.send_serv_response(clnt_socket, response)
                if user_in.logged_in:
                    self.logged_in_user = user_in.logged_in_user()
                    break

            if data == "exit":
                print(f"Connection with {addr[0]} terminated")
                break

#=============logged user============================

    def read_recvd_msgs(self, clnt_socket):
        



#self.logged_in_user


    def logged_user(self, clnt_socket, addr):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in self.user_menu: 
                response = {"bad command:": data}
                print(response)
                self.send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                self.logged_in_user.send_msg(clnt_socket, self.user_menu)



            if data == "read":




                
                self.logged_in_user.read_received_msgs(clnt_socket, self.user_menu)   
            if data == "mailbox": 
                self.logged_in_user.read_received_msgs(clnt_socket, self.user_menu, "")
            if data == "sent":
                self.logged_in_user.read_sent_msgs(clnt_socket, self.user_menu, "")
            if data == "exit":
                print(f"Connection with {addr[0]} terminated")
                break
   # admin permissions 
            if data in self.serv_info:
                self.logged_in_user.send_serv_info(clnt_socket, data, self.serv_start,self.version, self.user_menu)
            if data == "users":
                self.logged_in_user.list_of_users(clnt_socket, self.user_menu)
            if data == "pass":
                self.logged_in_user.change_password(clnt_socket, self.user_menu)
            if data == "delete":
                self.logged_in_user.delete_account(clnt_socket, self.user_menu)

    def handle_client(self, clnt_socket, addr):
        with clnt_socket:
            self.start_user_connection(clnt_socket, addr)
            self.logged_user(clnt_socket, addr)
