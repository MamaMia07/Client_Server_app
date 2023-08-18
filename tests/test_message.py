import unittest
from unittest import mock
import sys, json
sys.path.append('E:\! PY ZeroToJunior\client_server_application')

import user, tools

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.msg = user.User("test")
        self.test_input = self.read_test_data("test_received_msgs")
        self.test_output = self.read_test_data("test_msgs_list")
##        input_data={ "20/07/2023 13:50:13": {
##                            "sender": "1 admin",
##                            "recipient": "test",
##                            "text": "1. message from admin to test",
##                            "message read": False,
##                            "creation date": "29/07/2023 16:51:58"},
##                        "22/07/2023 16:51:58": {
##                            "sender": "2 admin",
##                            "recipient": "test",
##                            "text": "2. message from admin to test",
##                            "message read": True,
##                            "creation date": "29/07/2023 16:51:58" }}
##        output_data={ "20/07/2023 13:50:13": {
##                            "sender": "1 admin",
##                            "recipient": "test",
##                            "text": "1. message from admin to test",
##                            "message read": False,
##                            "creation date": "29/07/2023 16:51:58"},
##                    "22/07/2023 16:51:58": {
##                            "sender": "2 admin",
##                            "recipient": "test",
##                            "text": "2. message from admin to test",
##                            "message read": True,
##                            "creation date": "29/07/2023 16:51:58" }}
    def read_test_data(self, file):
        with open(file, "r") as outfile:
            data = outfile.read()
            data = json.loads(data)
        return data

    def test_get_msgs_list(self):
        pass
##
    def test_insert_username(self):
        pass
##        with mock.patch('user.read_from_file', return_value = self.input_data):
##            #with mock.patch('user.save_file.__builtin__.open', mock.mock_open(read_data=None)) as m:
##            with mock.patch('user.save_file', return_value = self.output_data):
##                
##                self.assertEqual(self.msg.read_msg("aa", ""),self.output_data)
##
        
if __name__ == '__main__':
    unittest.main()   

