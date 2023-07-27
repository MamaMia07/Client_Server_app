import account 
import user
from  tools import BasicMethods as bm


class ClntServCommunication():
    def __init__(self):
        self.start = {"Type":"",
                      " sign:":"to sign in",
                      " new:": "to register",
                      " exit:": "to disconnect"}
        self.user_menu = {"Type":"",
                      " new :":"to send message",
                      " box:": "to read messages",
                      " exit:": "to disconnect"}

    def new_account(self, clnt_socket, start):
        client_registration = account.NewUserRegistration()
        client_registration.new_user_data_setting(clnt_socket,start)
        

    def sign_in(self, clnt_socket, start, user_menu):
         user_signin = account.SignInUser()
         user_signin.sign_in_user(clnt_socket, start, user_menu)
         return user_signin
         
         

    def log_out(self):
        pass
                
    def user_connection(self, clnt_socket, addr):
        print(f"Connected with {addr[0]}")
        welcome = {"Welcome to my tiny server! :)":"\n"}
        response =  {**welcome , **self.start}
        bm().send_serv_response(clnt_socket, response)
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in ["sign", "new", "exit"]:
                response = {"bad command:": data}
                print(response)
                bm().send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                self.new_account(clnt_socket, self.start)
                data = clnt_socket.recv(1024).decode("utf-8")
            if data == "sign":
                sign_in = self.sign_in(clnt_socket, self.start, self.user_menu)
                if sign_in.status == "user":
                    logged_user = user.User(sign_in.username, sign_in.status)
##                        print(f"name logged: {logged_user.username}")
##                        print(f"status logged: {logged_user.status}")
                    break
                if sign_in.status == "admin":
                    logged_user = user.Admin(sign_in.username, sign_in.status)
                    break
            if data == "exit":
                print("Connection terminated")
                break
        
                    
            
#DOSTOSOWAC DO USERA I ADMINA wraz z class Response    
    def logged_user(self, clnt_socket):
        while True:
            data = clnt_socket.recv(1024).decode("utf-8")
            if data not in ["new", "box", "exit"]:
                response = {"bad command:": data}
                print(response)
                bm().send_serv_response(clnt_socket, response)
                continue
            if data == "new":
                print("jest NEW")
                break
##                data = clnt_socket.recv(1024).decode("utf-8")
##                print(data)
##                response = resp.prep_serv_response(data)
##                print(response)
##                clnt_conn_socket.sendall(response.encode("utf-8"))
##                if data == "stop":
##                    print("Connection terminated")
##                    break


    def handle_client(self, clnt_socket, addr):
        with clnt_socket:
            self.user_connection(clnt_socket, addr)
            self.logged_user(clnt_socket)
