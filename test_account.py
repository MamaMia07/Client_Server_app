import unittest
#import sys
#sys.path.append('E:\! PY ZeroToJunior\client_server_application')
import account
#from  tools import BasicMethods as bm
nur = account.NewUserRegistration()
siu = account.SignInUser()

class TestNewAccount(unittest.TestCase):
    
##    def test_insert_username(self):
##        newdata={"admin":{f"username admin": "already exists\nusername:"},
##              "aa3z%#" : {f"username aa3z%# contains invalid char": "\nusername:"},
##              "" : {f"username ": "can not be empty\nusername:"},
##              "jola": True}
##        for key in newdata:
##            self.assertEqual(nur.insert_username(key), newdata[key])
    def test_insert_name_empty(self):
        us = {f"name ": "can not be empty"}
        self.assertEqual(nur.insert_name(""), us)
    def test_insert_name_OK(self):
        #self.assertEqual(nur.insert_name("MamaMia"), True)
        self.assertTrue(nur.insert_name("MamaMia"))

    def test_insert_username_exists(self):
        admin= {f"username admin": "already exists\nusername:"}
        self.assertEqual(nur.insert_username("admin"), admin)
    def test_insert_username_firb(self):
        us = {f"username aa3z%# contains invalid char": "\nusername:"}
        self.assertEqual(nur.insert_username("aa3z%#"), us)
    def test_insert_username_empty(self):
        us = {f"username ": "can not be empty\nusername:"}
        self.assertEqual(nur.insert_username(""), us)
    def test_insert_username_OK(self):
        #self.assertEqual(nur.insert_username("jola"), True)
        self.assertTrue(nur.insert_username("jola"))

    def test_insert_password_short(self):
        resp = {"password should have at least":"4 characters\npassword:"}
        self.assertEqual(nur.insert_password("a", "abcde"),resp)
    def test_insert_password_diff(self):
        resp = {"two different passwords have been entered":"\npassword:"}
        self.assertEqual(nur.insert_password("wwww", "2"),resp)
    def test_insert_password_OK(self):
        #self.assertEqual(nur.insert_password("123456", "123456"),True)
        self.assertTrue(nur.insert_password("123456", "123456"))



class TestSignInUser(unittest.TestCase):

    def test_check_user_OK(self):
        #self.assertEqual(siu.check_user("testowy"),True)
        self.assertTrue(siu.check_user("testowy"))
    def test_check_user_false(self):
        #self.assertEqual(siu.check_user("testowy111"),False)
        self.assertFalse(siu.check_user("testowy111"))

    def test_check_password_OK(self):
        #self.assertEqual(siu.check_password("testowy", "12345"),True)
        self.assertTrue(siu.check_password("testowy", "12345"))
        
    def test_check_password_false1(self):
        #self.assertEqual(siu.check_password("testowy1111", "12345"),False)
        self.assertFalse(siu.check_password("testowy1111", "12345"))
    def test_check_password_false2(self):
        #self.assertEqual(siu.check_password("testowy", "123456"),False)
        self.assertFalse(siu.check_password("testowy", "123456"))

    def test_sign_in_user(self):
        siu = account.SignInUser()
        resp = (True, "testowy", "user")
        self.assertEqual(siu.sign_in_user("testowy", "12345"),resp)
    def test_sign_in_user_None(self):
        siu = account.SignInUser()
        resp = (False, "", "")
        self.assertEqual(siu.sign_in_user("testowy1111", "12345"),resp)
    
    
    
        
if __name__ == '__main__':
    unittest.main()   

