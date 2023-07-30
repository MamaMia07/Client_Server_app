import datetime
from  tools import BasicMethods as bm


class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status
        self.path = f"users/{self.username}/"

    def send_msg(self, clnt_socket, user_menu):
        new_msg = Message(self.username)
        new_msg.create_and_send_msg(clnt_socket, user_menu)

    def read_msg(self, clnt_socket, user_menu):
        path_file = self.path + "received_msgs.json"
        message_box = bm().read_from_file(path_file)
        for key in message_box:
            if message_box[key]["message read"] == False:
                print(message_box[key]["message read"])
                msg = {"from:" : message_box[key]["sender"],
                   "date:" : message_box[key]["creation date"],
                   "text:\n" : message_box[key]["text"] }
              
                message_box[key]["message read"] = True
                print(message_box[key]["message read"])
                nextmsg = {"next message?": "y/n"}
                msg.update(nextmsg)
                bm().send_serv_response(clnt_socket, msg)
                while True:
                    answ = clnt_socket.recv(1024).decode("utf-8")
                    if answ in[ "n", "y"]: break
                if answ == "n":
                    bm().send_serv_response(clnt_socket, user_menu)
                    break
        bm().save_file(path_file, message_box)
        finish = {"All messages are read.": "\n"}
        finish.update(user_menu)
        bm().send_serv_response(clnt_socket, finish)
        
    


# DLA USERA- OPCJA ZMIANY HASLA
# if cmd = "exit" -__>  clnt_conn_socket.close()




class Admin(User):
    def __init__(self, username, status="admin"):
        self.username = username
        self.status = status
        self.path = f"users/{self.username}/"






class Message():
    def __init__(self, sender):
        self.sender = sender
        self.recipient = ""
        self.text = ""
        self.date = ""

    def create_message(self):
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message = { self.date: {"sender" :  self.sender,
                    "recipient" : self.recipient,
                    "text" :  self.text,
                    "message read" : False,
                    "creation date" : self.date}}
        return message

    def set_recipient(self, clnt_socket):
        self.recipient = self.enter_recipient(clnt_socket)

    def set_text(self, clnt_socket):
        self.text = self.enter_msg_text(clnt_socket)

    def enter_recipient(self,clnt_socket):
        users = bm().read_from_file("admin/users.json")
        users_list = [key for key in users]
        print(users_list)
        while True:
            recvd_recipient = clnt_socket.recv(1024).decode("utf-8")
            recvd_recipient = recvd_recipient.lower().strip()
            if recvd_recipient not in users_list : 
                response = {f"username {recvd_recipient}": "does not exist\nrecipient:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            elif recvd_recipient == "" :
                response = {f"username": "can not be empty\nrecipient:"}
                bm().send_serv_response(clnt_socket, response)
                continue
            else: break
        return recvd_recipient

    def enter_msg_text(self,clnt_socket):
        while True:
            recvd_text = clnt_socket.recv(1024).decode("utf-8")
            if recvd_text == " " :
                response = {f"username": "can not be empty\nrecipient:"}
                bm().send_serv_response(clnt_socket, response)
            elif len(recvd_text) > 255:
                response = {f"text limit is 255 characters\n":"please\
 abbreviate the text\nmessage content:"}
                bm().send_serv_response(clnt_socket, response)
            else: break
        return recvd_text

    def nmb_not_read_msgs(self,name, file):
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
        print(f"\n\nzapisana tresc wiadomości\nod {self.sender}\ndo {self.recipient}\n{self.text}")
        try:
            msg_list = bm().read_from_file(recip_file_path)
            msg_list.update(new_msg)
        except: msg_list = new_msg
        bm().save_file(file_path, msg_list)


    def create_and_send_msg(self, clnt_socket, user_menu):
        response = {"\nCreating new message":"\nenter the message recipier:"} 
        bm().send_serv_response(clnt_socket, response)
        self.set_recipient(clnt_socket)
        print(f"zapisane odbiorca: {self.recipient}")

        response= {"message content:":""}
        bm().send_serv_response(clnt_socket, response)
        self.set_text(clnt_socket)
        print(f"zapisana tresc wiadomości:\n {self.text}")
        while True:
            response = {"Send the message?":"y/n ?"} 
            bm().send_serv_response(clnt_socket, response)
            confirm = clnt_socket.recv(1024).decode("utf-8")
            if confirm  in ["y", "n"]:
                recipier_box = self.nmb_not_read_msgs(self.recipient, "received_msgs.json")
                if confirm == "y":
                    if recipier_box < 5:
                        new_message = self.create_message()
                        self.save_msg(new_message, self.recipient, "received_msgs.json")
                        self.save_msg(new_message, self.sender, "sent_msgs.json")
                        response= {"message has been sent.":"\n"}
                        response.update(user_menu)
                    else:
                        response= {"message can not be sent":"- recipier's meeeage box ........."}
                        response.update(user_menu)
                else:
                    response = {f"message not sent.":"\n"}
                    response.update(user_menu)
                bm().send_serv_response(clnt_socket, response)
                break

