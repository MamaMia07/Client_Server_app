import time 
import database as db

class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status

    def send_msg(self):
        new_msg = Message(self.username)
        return new_msg

    def read_old_msgs(self):
        message_box = db.select_messages_to(self.username)
        msg_status = ""
        return self.read_msg(self.username, msg_status, message_box)

    def read_new_msgs(self):
        message_box = db.select_messages_to(self.username)
        msg_status = True
        return self.read_msg(self.username, msg_status, message_box)


    def read_sent_msgs(self):
        message_box = db.select_messages_from(self.username)
        msg_status = ""
        return self.read_msg(self.username, msg_status, message_box)


    def mark_msg_read(self, msg_id):
        db.mark_msg_read(msg_id)


    def get_msgs_list(self,username, msg_status, message_box):
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
        try:
            response = self.get_msgs_list(username, msg_status, message_box)
            finish = {"":{"All messages are read.": ""}}
            response.update(finish)
        except: response = {'':{"There is no message": ""}}
        return response




class Admin(User):

    def send_serv_info(self, data, serv_start, ver):
        server_life = time.time() - serv_start
        serv_info = {"info": {"server v.:": f"{ver}\n"},
                         "uptime": {"server uptime:": f"{server_life:.4f}s\n"}}
        return serv_info[data]


    def list_of_users(self):
        users_list = db.select_users()
        username_list = [user[0] for user in users_list] 
        response = {"list of users:\n": f"{username_list}\n"}
        return response


    def change_password(self, username, new_passw):
        if db.change_pswrd(new_passw, username):
            response = {f"new passwrd for {username} saved":"\n"}
        else: response = {f"user {username} does not exist":"\n"}
        return response

    def delete_account(self, username):
        if db.change_status(username, False):
            response = {f"account {username} has been deactivated.":"\n"}
        else: response = {f"user {username} does not exist":"\n"}
        return response



class Message():
    def __init__(self, sender):
        self.sender = sender
        self.recipient = ""
        self.content = ""


    def enter_recipient(self,recvd_recipient):
        users_list = db.select_active_users()
        recvd_recipient = recvd_recipient.lower().strip()
        if not any(user[0] == recvd_recipient for user in users_list):
            response = {f"username {recvd_recipient}": "does not exist\nrecipient:"}
        else:
            self.recipient = recvd_recipient
            response = True
        return response 


    def enter_msg_content(self,recvd_text):
        recvd_text.strip()
        if len(recvd_text) > 255:
            response = {"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
        else:
            self.content = recvd_text
            response = True
        return response 


    def send_new_msg(self, confirm):
        recipient_box = db.nbr_of_unread_msgs(self.recipient)
        if confirm == "y":
            if recipient_box[0][0] < 5:
                db.new_message(self.sender, self.recipient, self.content)
                response= {"Message has been sent.":""}
            else:
                response= {"Message was not delivered, ":f"{self.recipient} inbox is full\n"}
        else:
            response = {f"Message not sent.":""}
        return response
