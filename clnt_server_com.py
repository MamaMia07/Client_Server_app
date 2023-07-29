import account 
import user
from  tools import BasicMethods as bm


class ClntServCommunication():
    def __init__(self, start_serv, version):
        
        self.help = {"stop" : ": disconnect",
                        "info": " : server software version",
                        "uptime": " : server uptime",
                        "help": " : menu help"}
        self.serv_start = start_serv
        self.version = version
        
        self.start_menu = {"Type":"",
                      "sign":": to sign in",
                      "new": ": to register",
                      "exit": ": to disconnect"}

        self.user_menu = {"Type":"",
                      "message" : ": to send message",
                      "new":  ": to rad new messages in mailbox",
                      "mailbox": ": to read all messages in mailbox",
                      "exit": ": to disconnect"}

## ===== DLA ADMINA=====================
##    def set_serv_response(self, cmd):
##        self.server_life = time.time() - self.start
##        self.responses = {"info": {"server v.:": self.version},
##                         "uptime": {"server uptime:": f"{self.server_life:.4f}s"},
##                         "stop" : {"connection status:": "terminated"},
##                         "help": self.help}
##        if cmd in self.responses:
##            return self.responses[cmd]
##        else:
##            return {"Unknown command.\nType 'help' for command list.":""}
## 
##    def prep_serv_response(self, cmd):
##        self.serv_resp = self.set_serv_response(cmd)
##        return json.dumps(self.serv_resp, indent = 4)
##

##===============================================

    def new_account(self, clnt_socket, start_menu):
        client_registration = account.NewUserRegistration()
        client_registration.new_user_data_setting(clnt_socket,start)
        

    def sign_in(self, clnt_socket, start_menu, user_menu):
         user_signin = account.SignInUser()
         user_signin.sign_in_user(clnt_socket, start_menu, user_menu)
         return user_signin
         
         

    def log_out(self):
        pass
                
    def user_connection(self, clnt_socket, addr):
        print(f"Connected with {addr[0]}")
        welcome = {"Welcome to my tiny server! :)":"\n"}
        response =  {**welcome , **self.start_menu}
        bm().send_serv_response(clnt_socket, response)
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in  self.start_menu: #["sign", "new", "exit"]:
                response = {"bad command:": data}
                print(response)
                bm().send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                self.new_account(clnt_socket, self.start_menu)
                data = clnt_socket.recv(1024).decode("utf-8")
            if data == "sign":
                sign_in = self.sign_in(clnt_socket, self.start_menu, self.user_menu)
                if sign_in.status == "user":
                    self.logged_in_user = user.User(sign_in.username, sign_in.status)
##                        print(f"name logged: {logged_user.username}")
##                        print(f"status logged: {logged_user.status}")
                    break
                if sign_in.status == "admin":
                    self.logged_in_user = user.Admin(sign_in.username, sign_in.status)
                    break
            if data == "exit":
                print("Connection terminated")
                break
        
                    
            
#DOSTOSOWAC DO USERA I ADMINA wraz z class Response    
    def logged_user(self, clnt_socket):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in self.user_menu: #["new", "box", "exit"]:
                response = {"bad command:": data}
                print(response)
                bm().send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                print("jest NEW")
                self.logged_in_user.send_msg(clnt_socket, self.user_menu)

            if data == "mailbox":
                print("jest SKRZYNKA")
                self.logged_in_user.read_msg(clnt_socket, self.user_menu)   
##                data = clnt_socket.recv(1024).decode("utf-8")
##                print(data)
##                response = resp.prep_serv_response(data)
##                print(response)
##                clnt_conn_socket.sendall(response.encode("utf-8"))
##                if data == "stop":
##                    print("Connection terminated")
##                    break
            if data == "exit":
                print("Connection terminated")
                break

    def handle_client(self, clnt_socket, addr):
        with clnt_socket:
            self.user_connection(clnt_socket, addr)
            self.logged_user(clnt_socket)
