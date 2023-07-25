import datetime, json
import hashlib, pathlib

def create_users_dir(username):
        path = pathlib.Path.cwd()/ "users"
        new_dir = path /username
        try:
            new_dir.mkdir()
        except FileExistsError:
            print("file already exists")

create_users_dir("oooo")
#==========================================
##users_lst = {"ola": 1, "isis":2}
##
##def get_username():
##        forbidden_symb = """`~!@#$%^&*() +={[}}|\:;"'<,>?/"""
##        forbidden = set(forbidden_symb)
##        while True:
##            username = (input("username: ")).strip().lower()
##            if username in users_lst:
##                print(f"username {username} already exists")
##            elif username == "":
##                print(f"username {username} can not be empty")
##            elif any(symbol in forbidden for symbol in username):
##                print(f"username {username} contains invalid char:\n{forbidden}")
##            else: break
##        print(f"username {username} accepted")
##get_username()
#=============================================================
#-------------------------------------------------------------

##
##username = (input("username: ")).strip().lower()
###test_string = "There are 2 apples for 4 persons"
## 
### initializing test list
##forbidden_symb = """`~!@#$%^&*()_-+={[}}|\:;"'<,>.?/ """
##forbidden = set(forbidden_symb)
##print(forbidden)
##
###forbidden = set(r"""`~!@#$%^&*()_-+={[}}|\:;"'<,>.?/ """)
###test_list = [" ","/","\\","'",'"',"*",'%', '&', '#', '@','^','$','+','(',')']
## 
### printing original string
##print("The original string : " + username )
## 
### printing original list
###print("The original list : " + str(test_list))
## 
### using list comprehension
### checking if string contains list element
##res = any(symbol in forbidden for symbol in username)
## 
### print result
##print("Does string contain any list element : " + str(res))

#----------------------------------------------------------

##has = "dupa2"
##m = hashlib.sha256()
##m.update(has.encode())
##haslo = m.hexdigest()
##print(haslo)
##
##m = hashlib.sha1()
##m.update(has.encode())
##haslo = m.hexdigest()
##print(haslo)

#=======HASLO ======================================
##
##def get_password():
##        #forbidden_symb = """`~!@#$%^&*() +={[}}|\:;"'<,>?/"""
##        #forbidden = set(forbidden_symb)
##        while True:
##            pass1 = (input("password: "))
##            pass2 = (input("repeat password: "))
##            if pass1 != pass2:
##                print("different passwords entered")
##            else: break
##        code = hashlib.sha256()
##        code.update(pass1.encode())
##        password = code.hexdigest()
##        print(f"password {password} saved")
##
##get_password()

#===========================================================
####dictionary = {"admin" :
####              { "status" : "admin",
####               "username" : "admin",
####               "password" : "dupa1",
####               "name" : "MamaMia07",
####               "creation date" : ""},
####              "test":
####              { "status" : "user",
####               "username" : "test",
####               "password" : "dupa2",
####               "name" : "NoName",
####               "creation date" : ""}
####              }
##
##dictionary = {"secondtest":
##              { "status" : "user",
##               "username" : "secondtest",
##               "password" : "dupa3",
##               "name" : "SecretName",
##               "creation date" : ""}
##              }
##
##       
###dictionary["admin"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
###dictionary["test"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
##
##dictionary["secondtest"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
##
##with open("sample.json", "r") as outfile:
##    data = outfile.read()
##
##data = json.loads(data)
##
##print(data)
##
##data.update(dictionary)
##print(data)
##
###print(dictionary)
### Serializing json
##json_object = json.dumps(data, indent=4)
## 
### Writing to sample.json
##with open("sample2.json", "w") as outfile:
##    outfile.write(json_object)
##
