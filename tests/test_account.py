import unittest
from unittest import mock
import sys 
sys.path.append('E:\...\client_server_application')

import account


class TestAccount(unittest.TestCase):
    
    def setUp(self):
        self.nur = account.NewUserRegistration()
        self.siu = account.SignInUser()
        self.userslist = [('test',), ('testowy',), ('admin',)]
        self.sign_in_user = [('test', '$2b$12$V9KWkFlFMm.HNkSXJHuFZeIAzvGgDowposCR/gJXQVZBNjvlPy0S6', 'user'),]
        
    def test_insert_name(self):
        name_empty = {f"name ": "can not be empty"}
        self.assertEqual(self.nur.insert_name(""), name_empty)
        self.assertTrue(self.nur.insert_name("MamaMia"))

    def test_insert_username(self):
        with mock.patch('account.db.select_users', return_value = self.userslist):
            user_exists = {f"username test": "already exists\nusername:"}
            self.assertEqual(self.nur.insert_username("test"), user_exists)

            user_forb = {f"username aa3z%# contains invalid char": "\nusername:"}
            self.assertEqual(self.nur.insert_username("aa3z%#"), user_forb)

            user_empty = {f"username ": "can not be empty\nusername:"}
            self.assertEqual(self.nur.insert_username(""), user_empty)

            self.assertTrue(self.nur.insert_username("jola"))

    def test_insert_password(self):
        passw_short = {"password should have at least":"4 characters\npassword:"}
        self.assertEqual(self.nur.insert_password("a", "abcde"),passw_short)

        passw_diff = {"two different passwords have been entered":"\npassword:"}
        self.assertEqual(self.nur.insert_password("wwww", "2"),passw_diff)

        self.assertTrue(self.nur.insert_password("123456", "123456"))


    def test_sign_in_user(self):
        siu = account.SignInUser()
        with mock.patch('account.db.user_log_data', return_value = self.sign_in_user):
            resp = (True, 'test', 'user')
            self.assertEqual(siu.sign_in_user('test', 'test'),resp)
    def test_sign_in_user_None1(self):
        siu = account.SignInUser()
        with mock.patch('account.db.user_log_data', return_value = self.sign_in_user):
            resp = (False, '', '')
            self.assertEqual(siu.sign_in_user('test2', 'test'),resp)
    def test_sign_in_user_None2(self):
        siu = account.SignInUser()
        with mock.patch('account.db.user_log_data', return_value = self.sign_in_user):
            resp = (False, "", "")
            self.assertEqual(siu.sign_in_user('test', '12345'),resp)
    
        
if __name__ == '__main__':
    unittest.main()   

