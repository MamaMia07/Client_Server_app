import unittest
from unittest import mock
import sys, json
sys.path.append('E:\! PY ZeroToJunior\client_server_application')

import user

class TestMessage(unittest.TestCase):
    
    def setUp(self):
        self.msg = user.Message()
        self.mailbox = self.read_test_data()

    def read_test_data(self):
        with open("test_received_msgs", "r") as outfile:
            data = outfile.read()
            data = json.loads(data)
        return data
