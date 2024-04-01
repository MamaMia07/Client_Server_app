import psycopg2, time, datetime
from configparser import ConfigParser
import bcrypt


def config(filename = 'database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return db


def connect(func):
    def wrapper(*args, **kwargs):
        record = None
        try:
            db_parameters = config()
            #print('\nConnecting to the PostgreSQL database...')
            connection = psycopg2.connect(**db_parameters)
            cursor = connection.cursor()

            postgres_query , values = func(*args, **kwargs)
            cursor.execute(postgres_query, values)
            connection.commit()
            try:
                record = cursor.fetchall()
            except:
                print("Nothing to fetch")
            print(f"Query {func.__name__} executed successfully")
        except (Exception, psycopg2.Error) as error:
             print("Error while connecting to PostgreSQL:\n",error)
        finally:
            if connection:  
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")  
        return record
    return wrapper


# hash password
def hash_pswrd(pswrd):
    salt = bcrypt.gensalt()
    print(bcrypt.hashpw(pswrd.encode(), salt))
    return (bcrypt.hashpw(pswrd.encode(), salt)).decode()


def check_password(recvd_pswrd, hashed_pswrd):
    return bcrypt.checkpw(recvd_pswrd.encode(), hashed_pswrd.encode())


# change password
@connect
def change_pswrd(pswrd, username):
    query = f"UPDATE users SET password = %s WHERE username = %s RETURNING id"
    values = (hash_pswrd(pswrd), username,) 
    return query, values


# new user to db - create new account
@connect
def save_new_account(username, pswrd, name): 
    query = f'''INSERT INTO users (username, password, name)
VALUES (%(username)s, %(password)s, %(name)s) RETURNING id'''          
    values = ({'username':username, 'password' :hash_pswrd(pswrd), 'name': name})              
    return query, values


# list of all users
@connect
def select_users():
    query = f"SELECT username FROM users"
    values = ()
    return query, values


# list of active users - potrzebne???
@connect
def select_active_users():
    query = f"SELECT username, role FROM active_users u JOIN roles ON u.role_id = roles.id"
    values = ()
    return query, values

  

# user's data for login
@connect
def user_log_data(username):
    query = f'''SELECT username, password, roles.role
FROM active_users u JOIN roles ON u.role_id = roles.id
WHERE username = %s '''
    values = (username,)
    return query, values


@connect
def set_login_date(username):
    query = f"UPDATE users SET last_log = now() WHERE username = %s RETURNING id"
    values = (username, )
    return query, values


#  change user's password
@connect
def change_status(username, status):
    query = f"UPDATE users SET active = %s WHERE username = %s RETURNING id"
    values = (status, username,)
    return query, values


#-------- MESSAGES ---------------------

# new message to db
@connect
def new_message(sender, recipient, content):
    query = f'''INSERT INTO messages (from_id, to_id, content)
VALUES ( 
(SELECT id FROM users WHERE username = %(sender)s),
(SELECT id FROM users WHERE username = %(recipient)s), 
%(content)s)
RETURNING id'''          
    values = ({'sender' : sender, 'recipient' :recipient, 'content' :content})              
    return query, values


# database results to dict
def db_res_to_dict(func):
    def wrapper(*args, **kwargs):
        db_result = func(*args, **kwargs)
        messages_list = {}
        for item in db_result:
            messages_list[item[0]] = {'msg_id': item[0],
                     'from' : item[1],
                     'to' : item[2],
                     'datetime' : item[4].strftime("%d.%m.%Y %H:%M:%S"),        
                     'content' : item[3].strip('"'),
                     'read' : item[5]
                     }
        return messages_list
    return wrapper
    


# messages TO user
@db_res_to_dict
@connect
def select_messages_to(username):
    query = f'''SELECT m.id, u1.username, u2.username, m.content, created_at, read
FROM messages m JOIN users u1 ON m.from_id = u1.id
JOIN users u2 ON m.to_id = u2.id
WHERE u2.username = %s
ORDER BY created_at DESC'''
    values = (username,)
    return query, values



# messages FROM user
@db_res_to_dict
@connect
def select_messages_from(username):
    query = f'''SELECT m.id, u1.username, u2.username, m.content, created_at, read
FROM messages m JOIN users u1 ON m.from_id = u1.id
JOIN users u2 ON m.to_id = u2.id
WHERE u1.username = %s
ORDER BY created_at DESC'''
    values = (username, )
    return query, values



# number of not read messages to user
@connect
def nbr_of_unread_msgs(username):
    query =f'''SELECT COUNT (*)
FROM messages m JOIN users u ON m.to_id = u.id
WHERE m.read = false AND u.username = %s '''
    values = (username, )
    return query, values


# set message status read - true
@connect
def mark_msg_read(msg_id):
    query = f"UPDATE messages SET read = true WHERE id = %s RETURNING id"
    values = (msg_id, )
    return query, values
