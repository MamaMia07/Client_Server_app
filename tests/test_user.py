import unittest
from unittest import mock
import sys, json
sys.path.append('E:\...\client_server_application')

import user

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.userslist = self.read_test_data("test_users.json")
        self.test_mailbox = self.read_test_data("test_received_msgs.json")
        self.test_msg_list = self.read_test_data("test_msgs_list.json")
        self.test_msg = user.Message("test")

    def read_test_data(self, file):
        with open(file, "r") as outfile:
            data = outfile.read()
            data = json.loads(data)
        return data

    def test_get_msgs_list(self):
        test_user = user.User("test")
        self.assertEqual(test_user.get_msgs_list(self.test_mailbox, ""), self.test_msg_list)    

    def test_enter_recipient(self):
        with mock.patch('user.read_from_file', return_value = self.userslist):
            exp_fake = {f"username fake_user": "does not exist\nrecipient:"}
            self.assertEqual(self.test_msg.enter_recipient("fake_user"), exp_fake)
            self.assertTrue(self.test_msg.enter_recipient("admin"))
            self.assertTrue(self.test_msg.recipient == "admin")

    def test_enter_msg_content(self):
        exp_resp = {"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
        self.assertEqual(self.test_msg.enter_msg_content("content"*100), exp_resp)
        self.assertTrue(self.test_msg.enter_msg_content("content"))
        self.assertTrue(self.test_msg.text , "content")

    def test_number_unread_msgs(self):
        with mock.patch('user.read_from_file', return_value = self.test_mailbox):
            self.assertEqual(self.test_msg.number_unread_msgs("", ""),2)
            

    def test_list_of_users(self):
        test_admin = user.Admin("admin")
        with mock.patch('user.read_from_file', return_value = self.userslist):
            exp_resp = {"list of users:\n": f"['admin', 'test']\n"}
            self.assertEqual(test_admin.list_of_users(), exp_resp )
            

if __name__ == '__main__':
    unittest.main()   

