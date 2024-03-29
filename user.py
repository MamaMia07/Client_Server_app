import time #, datetime, shutil
#from  tools import *
import database as db

class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status
        #self.path = f"users/{self.username}/"

    def send_msg(self):
        new_msg = Message(self.username)
        return new_msg

## DO POPRAWY
    def read_old_msgs(self):
        message_box = db.select_messages_to(self.username)
        msg_status = ""
        #file = self.username + "_received_msgs.json"
        return self.read_msg(self.username, msg_status, message_box)

    def read_new_msgs(self):
        message_box = db.select_messages_to(self.username)
        msg_status = True
        #file = self.username+"_received_msgs.json"
        return self.read_msg(self.username, msg_status, message_box)


    def read_sent_msgs(self):
        message_box = db.select_messages_from(self.username)
        msg_status = ""
#        file = self.username + "_sent_msgs.json"
        return self.read_msg(self.username, msg_status, message_box)


    def mark_msg_read(self, msg_id):
        db.mark_msg_read(msg_id)


    def get_msgs_list(self,username, msg_status, message_box):
        #message_box = db.select_messages_to(username)
        msg = {}
        for key in message_box:
            if message_box[key]["read"] != msg_status:
                msg[key] ={"from:" : message_box[key]["from"],
                       "to:" : message_box[key]["to"],
                       "date:" : message_box[key]["datetime"],
                       "content:\n" : message_box[key]["content"]
                        }
                response = msg
        return response

    def read_msg(self, username, msg_status, message_box ):
#        path_file = self.path + file
        try:
            #message_box = read_from_file(path_file)
            response = self.get_msgs_list(username, msg_status, message_box)
            finish = {"":{"All messages are read.": ""}}
            response.update(finish)
#            save_file(path_file, message_box)
        except: response = {'':{"There is no message": ""}}
        return response




class Admin(User):

    def send_serv_info(self, data, serv_start, ver):
        server_life = time.time() - serv_start
        serv_info = {"info": {"server v.:": f"{ver}\n"},
                         "uptime": {"server uptime:": f"{server_life:.4f}s\n"}}
        return serv_info[data]

## chyba ok 
    def list_of_users(self):
        users_list = db.select_users()
        #users_list = read_from_file("admin/users.json")
        username_list = [user[0] for user in users_list] 
        response = {"list of users:\n": f"{username_list}\n"}
        return response


#chyba OK
    def change_password(self, username, new_passw):
        if db.change_pswrd(new_passw, username):

##        users_list = read_from_file("admin/users.json")
##        if user_account in users_list:
##            users_list[user_account]["password"] = new_passw
##            save_file("admin/users.json", users_list)
            response = {f"new passwrd for {username} saved":"\n"}
        else: response = {f"user {username} does not exist":"\n"}
        return response

  # chyba OK  
    def delete_account(self, username):
        if db.change_status(username, False):

##        users_list = read_from_file("admin/users.json")
##        if user_account in users_list:
##            del users_list[user_account]
##            save_file("admin/users.json", users_list)
##            path = "users/" + user_account
##            shutil.rmtree(path)
            response = {f"account {username} has been deactivated.":"\n"}
        else: response = {f"user {username} does not exist":"\n"}
        return response



class Message():
    def __init__(self, sender):
        self.sender = sender
        self.recipient = ""
        self.content = ""
        #self.date = ""

##    def set_new_message(self):
##        #self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
##        message = { self.date: {"sender" :  self.sender,
##                    "recipient" : self.recipient,
##                    "text" :  self.text,
##                    "message read" : False,
##                   # "creation date" : self.date
##                    }}
##        return message


# chyba ok
    def enter_recipient(self,recvd_recipient):
        #users_list = read_from_file("admin/users.json")
        users_list = db.select_active_users()
        recvd_recipient = recvd_recipient.lower().strip()
        if not any(user[0] == recvd_recipient for user in users_list):
#        if recvd_recipient not in users_list : 
            response = {f"username {recvd_recipient}": "does not exist\nrecipient:"}
        else:
            self.recipient = recvd_recipient
            response = True
        return response 


#chyba ok
    def enter_msg_content(self,recvd_text):
        recvd_text.strip()
        if len(recvd_text) > 255:
            response = {"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
        else:
            self.content = recvd_text
            response = True
        return response 

# przerobione - NIEPOTRZEBNE ?
#    def number_unread_msgs(self, username):
#        return db.nbr_of_unread_msgs(username)



##        file_path = f"users/{name}/" + file
##        not_read_msgs = 0
##        try:
##            message_box = read_from_file(file_path)
##            for key in message_box:
##                if message_box[key]["message read"] == False:
##                    not_read_msgs += 1
##            return not_read_msgs
##        except: return 0
        
##    def save_msg(self):
##        db.new_message(self.sender, self.recipient, self.content)
        
##        file_path = f"users/{name}/" + file  
##        try:
##            msg_list = read_from_file(file_path)
##            msg_list.update(new_msg)
##        except: msg_list = new_msg
##        save_file(file_path, msg_list)


# chyba OK
    def send_new_msg(self, confirm):
        #recipier_box = self.number_unread_msgs(self.recipient, self.recipient+"_received_msgs.json")
        recipient_box = db.nbr_of_unread_msgs(self.recipient)
##        print(recipient_box)
##        print(recipient_box[0][0])
        #db.new_message(self.sender, self.recipient, self.content)
        
        if confirm == "y":
            if recipient_box[0][0] < 5:
                db.new_message(self.sender, self.recipient, self.content)
##                new_msg = self.set_new_message()
##                self.save_msg(new_msg , self.recipient, self.recipient + "_received_msgs.json")
##                self.save_msg(new_msg , self.sender, self.sender+"_sent_msgs.json")
                response= {"Message has been sent.":""}
            else:
                response= {"Message was not delivered, ":f"{self.recipient} inbox is full\n"}
        else:
            response = {f"Message not sent.":""}
        return response
