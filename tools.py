import datetime, json, pathlib, hashlib

class BasicMethods():
    def __init__(self):
        pass

    @staticmethod
    def send_serv_response(clnt_socket, resp):
        response= json.dumps(resp, indent = 4)
        clnt_socket.sendall(response.encode("utf-8"))


    @staticmethod
    def read_from_file(file_path):
        #file_path = path/file
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
##    @staticmethod
##    def update_json(json_obj, new_obj):
##        json_obj.update(new_obj)


    @staticmethod
    def create_users_dir(username):
        path = pathlib.Path.cwd()/ "users"
        new_dir = path /username
        try:
            new_dir.mkdir()
        except :# FileExistsError:
            print("file already exists")
        
