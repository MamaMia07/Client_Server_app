import json

start_menu = {"Type":"",
                      "sign":": to sign in",
                      "new": ": to register",
                      "exit": ": to disconnect"}

path_file = f"users/rewq/user_msgs.json"

def read_from_file(path_file):
        #file_path = path/file
        try:
            with open(path_file, "r") as outfile:
                data = outfile.read()
                data = json.loads(data)
            return data
        except json.decoder.JSONDecodeError:
            print(f"file {file_path} can not be read")
        except: print(f"file {file_path} content not available")

message_box = read_from_file(path_file)
print(path_file)

message_box.update({"":start_menu})
print(message_box)
