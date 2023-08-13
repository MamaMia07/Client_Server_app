import datetime, json, pathlib, hashlib

class BasicMethods():
    def __init__(self):
        pass

    @staticmethod
    def read_from_file(file_path):
        try:
            with open(file_path, "r") as outfile:
                data = outfile.read()
                data = json.loads(data)
            return data
        except json.decoder.JSONDecodeError:
            print(f"file {file_path} can not be read")
        except: print(f"file {file_path} content not available")

    @staticmethod
    def save_file(file, data):
        json_object = json.dumps(data, indent=4)
        try:
            with open(file, "w") as outfile:
                outfile.write(json_object)
        except: print(f"file {file} not saved")

    @staticmethod
    def code_password(passw):
        code = hashlib.sha256()
        code.update(passw.encode())
        password = code.hexdigest()
        return password

    @staticmethod
    def create_users_dir(username):
        path = pathlib.Path.cwd()/ "users"
        new_dir = path /username
        try:
            new_dir.mkdir()
        except :
            print("file already exists")
        
