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
    return (bcrypt.hashpw(pswrd.encode(), salt)).decode()


def check_password(recvd_pswrd, hashed_pswrd):
    return bcrypt.checkpw(recvd_pswrd.encode(), hashed_pswrd.encode())



queries = {'change_pswrd' : f"UPDATE users SET password = %s WHERE username = %s RETURNING id",
       'save_new_account' : f'''INSERT INTO users (username, password, name)
VALUES (%(username)s, %(password)s, %(name)s) RETURNING id''',
       'select_users' : "SELECT username FROM users",
       'select_active_users' : "SELECT username, role FROM active_users u JOIN roles ON u.role_id = roles.id",
       'user_log_data' : f'''SELECT username, password, roles.role
FROM active_users u JOIN roles ON u.role_id = roles.id
WHERE username = %s ''',
       'set_login_date' : f"UPDATE users SET last_log = now() WHERE username = %s RETURNING id",
       'change_status' : f"UPDATE users SET active = %s WHERE username = %s RETURNING id",
       'new_message' : f'''INSERT INTO messages (from_id, to_id, content)
VALUES ( 
(SELECT id FROM users WHERE username = %s),
(SELECT id FROM users WHERE username = %s), 
%s) RETURNING id''' ,
       'nbr_of_unread_msgs' : f'''SELECT COUNT (*) FROM messages m JOIN users u ON m.to_id = u.id
WHERE m.read = false AND u.username = %s ''',
        'mark_msg_read' :  f"UPDATE messages SET read = true WHERE id = %s RETURNING id",
           
       }



@connect
def db_query(db_query, values = ()):
    return db_query, values



##print(db_query(queries['select_users']))
##print(db_query(queries['user_log_data'], ('test',)))
##print(db_query(queries['set_login_date'], ('admin',)))
##print(db_query(queries['change_status'], (True, 'bambik')))

##print(db_query(queries['new_message'], ('admin', 'bambik', 'wiadomosc od admin do bambik')))
##print(db_query(queries['nbr_of_unread_msgs'], ('bambik',)))
##print(db_query(queries['mark_msg_read'], (26,)))


#-------- get MESSAGES ---------------------

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


##print(select_messages_to('admin'))

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
##print('')
##print(select_messages_from('admin'))
