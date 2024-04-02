import unittest
from unittest import mock
import sys
sys.path.append('E:\...\client_server_application')

import user

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.userslist = [('test',), ('testowy',), ('admin',)]
        self.test_mailbox = {98: {'msg_id': 98,
                                  'from': 'test',
                                  'to': 'admin',
                                  'datetime': '28.03.2024 12:07:35',
                                  'content': ' info od test do admin',
                                  'read': False},
                             99: {'msg_id': 99,
                                  'from': 'test 1',
                                  'to': 'test',
                                  'datetime': '28.03.2024 12:12:25',
                                  'content': ' info od test_1 do admin',
                                  'read': False}
                             }

        self.test_msg_list = {98: {'from:': 'test',
                                  'to:': 'admin',
                                  'date:': '28.03.2024 12:07:35',
                                  'content:\n': ' info od test do admin',
                                  },
                             99: {'from:': 'test 1',
                                  'to:': 'test',
                                  'date:': '28.03.2024 12:12:25',
                                  'content:\n': ' info od test_1 do admin',
                                  }
                             }
        self.test_msg = user.Message('test')


    def test_get_msgs_list(self):
        test_user = user.User('test')
        self.assertEqual(test_user.get_msgs_list('test', '', self.test_mailbox), self.test_msg_list)    

    def test_enter_recipient(self):
        with mock.patch('user.db.select_active_users', return_value = self.userslist):
            exp_fake = {f"username fake_user": "does not exist\nrecipient:"}
            self.assertEqual(self.test_msg.enter_recipient("fake_user"), exp_fake)
            self.assertTrue(self.test_msg.enter_recipient("admin"))
            self.assertTrue(self.test_msg.recipient == "admin")

    def test_enter_msg_content(self):
        exp_resp = {"\ntext limit is 255 characters,":"please\
 abbreviate the text\nmessage content:"}
        self.assertEqual(self.test_msg.enter_msg_content("content"*100), exp_resp)
        self.assertTrue(self.test_msg.enter_msg_content("content"))
        self.assertTrue(self.test_msg.content , "content")

            

    def test_list_of_users(self):
        test_admin = user.Admin("admin")
        with mock.patch('user.db.select_users', return_value = self.userslist):
            exp_resp = {"list of users:\n": f"['test', 'testowy', 'admin']\n"}
            self.assertEqual(test_admin.list_of_users(), exp_resp )
            

if __name__ == '__main__':
    unittest.main()   

