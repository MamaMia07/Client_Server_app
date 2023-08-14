import time, datetime, shutil
from  tools import BasicMethods as bm


class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status
        self.path = f"users/{self.username}/"

    def send_msg(self):
        new_msg = Message(self.username)
        return new_msg

    def read_old_msgs(self):
        read_msg_stat = ""
        file = self.username + "_received_msgs.json"
        return self.read_msg(file, read_msg_stat)

    def read_new_msgs(self):
        read_msg_stat = True
        file = self.username+"_received_msgs.json"
        return self.read_msg(file, read_msg_stat)

    def read_sent_msgs(self): 
        read_msg_stat = ""
        file = self.username + "_sent_msgs.json"
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
    def send_serv_info(self, data, serv_start, ver):
        server_life = time.time() - serv_start
        serv_info = {"info": {"server v.:": f"{ver}\n"},
                         "uptime": {"server uptime:": f"{server_life:.4f}s\n"}}
        return serv_info[data]
 
    def list_of_users(self):
        users_list = bm().read_from_file("admin/users.json")
        username_list = [key for key in users_list] 
        response = {"list of users:\n": f"{username_list}\n"}
        return response

    def change_password(self, user_account, new_passw):
        users_list = bm().read_from_file("admin/users.json")
        if user_account in users_list:
            users_list[user_account]["password"] = new_passw
            bm().save_file("admin/users.json", users_list)
            response = {f"new passwrd for {user_account} saved":"\n"}
        else: response = {f"user {user_account} does not exist":"\n"}
        return response
    
    def delete_account(self, user_account):
        users_list = bm().read_from_file("admin/users.json")
        if user_account in users_list:
            del users_list[user_account]
            bm().save_file("admin/users.json", users_list)
            path = "users/" + user_account
            shutil.rmtree(path)
            response = {f"account {user_account} removed.":"\n"}
        else: response = {f"user {user_account} does not exist":"\n"}
        return response



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

    def enter_recipient(self,recvd_recipient):
        users_list = bm().read_from_file("admin/users.json")
        recvd_recipient = recvd_recipient.lower().strip()
        if recvd_recipient not in users_list : 
            response = {f"username {recvd_recipient}": "does not exist\nrecipient:"}
        elif recvd_recipient == "" :
            response = {f"username": "can not be empty\nrecipient:"}
        else:
            self.recipient = recvd_recipient
            response = True
        return response 

    def enter_msg_text(self,recvd_text):
        recvd_text.strip()
        if recvd_text == "" :
            response = {f"username": "can not be empty\nrecipient:"}
        elif len(recvd_text) > 255:
            response = {f"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
        else:
            self.text = recvd_text
            response = True
        return response 

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

    def send_new_msg(self, confirm):
        recipier_box = self.number_unread_msgs(self.recipient, self.recipient+"_received_msgs.json")
        if confirm == "y":
            if recipier_box < 5:
                new_msg = self.set_new_message()
                self.save_msg(new_msg , self.recipient, self.recipient + "_received_msgs.json")
                self.save_msg(new_msg , self.sender, self.sender+"_sent_msgs.json")
                response= {"Message has been sent.":""}
            else:
                response= {"Message was not delivered, ":f"{self.recipient} inbox is full\n"}
        else:
            response = {f"Message not sent.":""}
        return response
