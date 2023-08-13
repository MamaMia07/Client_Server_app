import time, datetime, shutil
from  tools import BasicMethods as bm


class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status
        self.path = f"users/{self.username}/"

    def send_msg(self, clnt_socket, user_menu):
        new_msg = Message(self.username)


        new_msg.send_new_msg(clnt_socket, user_menu)


    def read_old_msgs(self):
        read_msg_stat = ""
        file = "received_msgs.json"
        return self.read_msg(file, read_msg_stat)

    def read_new_msgs(self):
        read_msg_stat = True
        file = "received_msgs.json"
        return self.read_msg(file, read_msg_stat)

    def read_sent_msgs(self): 
        read_msg_stat = ""
        file = "sent_msgs.json"
        return self.read_msg(file, read_msg_stat)


    def read_msg(self, file, read_msg_stat):
        path_file = self.path + file 
        try:
            message_box = bm().read_from_file(path_file)
            msg = {}
            for key in message_box:
                if message_box[key]["message read"] != read_msg_stat:
                    msg[key] ={"from:" : message_box[key]["sender"],
                           "to:" : message_box[key]["recipient"],
                           "date:" : message_box[key]["creation date"],
                           "text:\n" : message_box[key]["text"]
                            }
                    message_box[key]["message read"] = True
                    response = msg
            finish = {"":{"All messages are read.": ""}}
            response.update(finish)
            bm().save_file(path_file, message_box)
        except: response = {'':{"There is no message": ""}}
        return response




class Admin(User):
    def send_serv_info(self, clnt_socket, data, serv_start, ver, user_menu):
        server_life = time.time() - serv_start
        serv_info = {"info": {"server v.:": f"{ver}\n"},
                         "uptime": {"server uptime:": f"{server_life:.4f}s\n"}}
        resp = {**serv_info[data], ** user_menu}
        bm().send_serv_response(clnt_socket, resp)
 
    def list_of_users(self, clnt_socket, user_menu):
        users_list = bm().read_from_file("admin/users.json")
        username_list = [key for key in users_list] 
        response = {"list of users:\n": f"{username_list}\n"}
        response.update(user_menu)
        bm().send_serv_response(clnt_socket, response)

    def change_password(self, clnt_socket, user_menu):
        users_list = bm().read_from_file("admin/users.json")
        response = {"Change user's passwrd:":"",
                    "enter username:" : ""} 
        bm().send_serv_response(clnt_socket, response)
        user_account = clnt_socket.recv(1024).decode("utf-8")
        if user_account in users_list:
            response = {"enter new user's password:":"\n"}
            bm().send_serv_response(clnt_socket, response)
            new_passw = clnt_socket.recv(1024).decode("utf-8")
            users_list[user_account]["password"] = new_passw
            bm().save_file("admin/users.json", users_list)
            response = {f"new passwrd for {user_account} saved":"\n"}
        else: response = {"user does not exist":"\n"}
        response.update(user_menu)
        bm().send_serv_response(clnt_socket, response)

    def delete_account(self, clnt_socket, user_menu):
        users_list = bm().read_from_file("admin/users.json")
        response = {"Deleting user's account:":"",
                    "enter username:" : ""} 
        bm().send_serv_response(clnt_socket, response)
        user_account = clnt_socket.recv(1024).decode("utf-8")
        if user_account in users_list:
            del users_list[user_account]
            bm().save_file("admin/users.json", users_list)
            path = "users/" + user_account
            shutil.rmtree(path)
            response = {f"account {user_account} removed.":"\n"}
        else: response = {"user does not exist":"\n"}
        response.update(user_menu)
        bm().send_serv_response(clnt_socket, response)


class Message():
    def __init__(self, sender):
        self.sender = sender
        self.recipient = ""
        self.text = ""
        self.date = ""

    def set_new_message(self):
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = { self.date: {"sender" :  self.sender,
                    "recipient" : self.recipient,
                    "text" :  self.text,
                    "message read" : False,
                    "creation date" : self.date}}
        return message

##    def set_recipient(self, clnt_socket):
##        self.recipient = self.enter_recipient(clnt_socket)
##
##    def set_text(self, clnt_socket):
##        self.text = self.enter_msg_text(clnt_socket)

    def enter_recipient(self,recvd_recipient):
        users_list = bm().read_from_file("admin/users.json")
##        while True:
##            recvd_recipient = clnt_socket.recv(1024).decode("utf-8")
        recvd_recipient = recvd_recipient.lower().strip()
        if recvd_recipient not in users_list : 
            response = {f"username {recvd_recipient}": "does not exist\nrecipient:"}
                #bm().send_serv_response(clnt_socket, response)
               # continue
        elif recvd_recipient == "" :
            response = {f"username": "can not be empty\nrecipient:"}
                #bm().send_serv_response(clnt_socket, response)
                #continue
        else:
            #self.recipient = recvd_recipient
            response = True
        return response #recvd_recipient


    def enter_msg_text(self,recvd_text):
##        while True:
##            recvd_text = clnt_socket.recv(1024).decode("utf-8")
        recvd_text.strip()
        if recvd_text == "" :
            response = {f"username": "can not be empty\nrecipient:"}
                #bm().send_serv_response(clnt_socket, response)
        elif len(recvd_text) > 255:
            response = {f"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
                #bm().send_serv_response(clnt_socket, response)
        else: response = True
        return response #recvd_text


    def number_unread_msgs(self,name, file):
        file_path = f"users/{name}/" + file
        not_read_msgs = 0
        try:
            message_box = bm().read_from_file(file_path)
            for key in message_box:
                if message_box[key]["message read"] == False:
                    not_read_msgs += 1
            return not_read_msgs
        except: return 0
        
    def save_msg(self, new_msg, name, file):
        file_path = f"users/{name}/" + file  
        try:
            msg_list = bm().read_from_file(file_path)
            msg_list.update(new_msg)
        except: msg_list = new_msg
        bm().save_file(file_path, msg_list)

##    def create_new_message(self, clnt_socket, user_menu):
##        response = {"\nCreating new message":"\nenter the message recipier:"} 
##        bm().send_serv_response(clnt_socket, response)
##        self.set_recipient(clnt_socket)
##        response= {"message content:":""}
##        bm().send_serv_response(clnt_socket, response)
##        self.set_text(clnt_socket)

    def send_new_msg(self, confirm):
        #self.create_new_message(clnt_socket, user_menu)
##        while True:
##            response = {"Send the message?":"y/n ?"} 
##            bm().send_serv_response(clnt_socket, response)
##            confirm = clnt_socket.recv(1024).decode("utf-8")
##            if confirm  in ["y", "n"]:
        recipier_box = self.number_unread_msgs(self.recipient, "received_msgs.json")
        if confirm == "y":
            if recipier_box < 5:
                new_message = self.set_new_message()
                self.save_msg(new_message, self.recipient, "received_msgs.json")
                self.save_msg(new_message, self.sender, "sent_msgs.json")
                response= {"Message has been sent.":"\n"}
                response.update(user_menu)
            else:
                response= {"Message was not delivered, ":f"{self.recipient} inbox is full\n"}
                response.update(user_menu)
            else:
                response = {f"Message not sent.":"\n"}
                #response.update(user_menu)
                #bm().send_serv_response(clnt_socket, response)
                #break
            return response
