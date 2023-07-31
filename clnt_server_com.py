import account 
import user
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

    def new_account(self, clnt_socket, start_menu):
        client_registration = account.NewUserRegistration()
        client_registration.new_user_data_setting(clnt_socket,start_menu)

    def sign_in(self, clnt_socket, start_menu, user_menu, adm_menu):
         user_signin = account.SignInUser()
         user_signin.sign_in_user(clnt_socket, start_menu, user_menu, adm_menu)
         return user_signin

    def user_connection(self, clnt_socket, addr):
        print(f"Connected with {addr[0]}")
        welcome = {"Welcome to my tiny server! :)":""}
        response =  {**welcome , **self.start_menu}
        bm().send_serv_response(clnt_socket, response)
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in  self.start_menu:
                response = {"bad command:": data}
                bm().send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                self.new_account(clnt_socket, self.start_menu)
                data = clnt_socket.recv(1024).decode("utf-8")
            if data == "sign":
                sign_in = self.sign_in(clnt_socket, self.start_menu, self.user_menu, self.admin_menu)
                if sign_in.status == "user":
                    self.logged_in_user = user.User(sign_in.username, sign_in.status)
                    print(f"{self.logged_in_user.username} logged in as {self.logged_in_user.status}")
                    break
                elif sign_in.status == "admin":
                    self.user_menu =  {**self.user_menu , **self.admin_menu}
                    self.logged_in_user = user.Admin(sign_in.username, sign_in.status)
                    print(f"{self.logged_in_user.username} logged in as {self.logged_in_user.status}")
                    break
            if data == "exit":
                print("Connection with {addr[0]} terminated")
                break

    def logged_user(self, clnt_socket):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in self.user_menu: 
                response = {"bad command:": data}
                print(response)
                bm().send_serv_response(clnt_socket, response)
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
                print("Connection terminated")
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
            self.user_connection(clnt_socket, addr)
            self.logged_user(clnt_socket)
