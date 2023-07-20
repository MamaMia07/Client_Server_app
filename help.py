import datetime, json
import hashlib

has = "dupa2"
m = hashlib.md5()
m.update(has.encode())
haslo = m.hexdigest()
print(haslo)

m = hashlib.sha1()
m.update(has.encode())
haslo = m.hexdigest()
print(haslo)
##dictionary = {"admin" :
##              { "status" : "admin",
##               "username" : "admin",
##               "password" : "dupa1",
##               "name" : "MamaMia07",
##               "creation date" : ""},
##              "test":
##              { "status" : "user",
##               "username" : "test",
##               "password" : "dupa2",
##               "name" : "NoName",
##               "creation date" : ""}
##              }

dictionary = {"secondtest":
              { "status" : "user",
               "username" : "secondtest",
               "password" : "dupa3",
               "name" : "SecretName",
               "creation date" : ""}
              }

       
#dictionary["admin"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#dictionary["test"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

dictionary["secondtest"]["creation date"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

with open("sample.json", "r") as outfile:
    data = outfile.read()

data = json.loads(data)

print(data)

data.update(dictionary)
print(data)

#print(dictionary)
# Serializing json
json_object = json.dumps(data, indent=4)
 
# Writing to sample.json
with open("sample2.json", "w") as outfile:
    outfile.write(json_object)

##with open("sample.json", "a") as outfile:
##    outfile.write(json_object)
##

##with open('sample.json', 'r') as openfile:
## 
##    # Reading from json file
##    json_object2 = json.load(openfile)
## 
##print(json_object2)
##print(type(json_object2))
