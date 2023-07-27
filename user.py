from  tools import BasicMethods as bm


class User():
    def __init__(self, username, status="user"):
        self.username = username
        self.status = status

    def read_msg(self):
        pass
        

class Admin(User):
    def __init__(self, username, status="admin"):
        self.username = username
        self.status = status
