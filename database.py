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
            # read connection parameters
            db_parameters = config()

            # connect to the PostgreSQL server
            print('\nConnecting to the PostgreSQL database...')
            connection = psycopg2.connect(**db_parameters)

            # Create a cursor to perform database operations
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
    values = (hash_pswrd(pswrd), username,) # MA BYC JUZ ZAHASHOWANE!!!!!
    return query, values

##print(change_pswrd('Nowe haselko-10 oli', 'ola'))

#### CZY POTRZEBNE?? 
##@connect
##def get_password(username):
##    query = f"SELECT password FROM users WHERE username = %s"
##    values = (username, )
##    return query , values
##
####print(f"z bazy hasło : {get_password('bambik')}")
####print(type(get_password('bambik')[0][0]))


# new user to db - create new account
@connect
def save_new_account(username, pswrd, name): 
    query = f'''INSERT INTO users (username, password, name)
VALUES (%(username)s, %(password)s, %(name)s) RETURNING id'''          
    values = ({'username':username, 'password' :hash_pswrd(pswrd), 'name': name})              
    return query, values

#print("Inserted user_id: ", save_new_account('test', hash_pswrd('test'), 'name test'), "\n")


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


##users = select_users()  
##print("Selected names: ", users)
##
##users_list = select_active_users()  
##print("Selected active names: ", users_list)
##print("rola danego uzytkownika" , users_list[1][1])
##
##for lst in users_list:
##    if "ola" in lst:
##        print(f"rola bambika: {lst[1]}")
##        break

    

# user's data for login
@connect
def user_log_data(username):
    query = f'''SELECT username, password, roles.role
FROM active_users u JOIN roles ON u.role_id = roles.id
WHERE username = %s '''
    values = (username,)
    return query, values

##name = 'bambik'
##user = user_log_data(name)
##print(user)
##user_pas = user[0][1] 
##print(f"username : {user[0][0]}")
##print(f"pswrd : {(user[0][1])}")
##print(f"role : {user[0][2]}")
##print("zakodowane tu")
##hashed = hash_pswrd(name) 
##print((hashed))
##print(user[0][1]== hashed)
##haslo = 'bambik'
##print(bcrypt.checkpw(haslo.encode(), user_pas.encode(),))
##print(check_password(haslo, user[0][1]))


##
##username_ind = [(i, users_list[i].index("bambik"))
##               for i in range(len(users_list)) if "bambik" in users_list[i]]
##
##print(username_ind[0][1])
##print(findItem(users_list, 'admin')) # [(0, 0)]
##print(findItem(users_list, 'bambik')) # [(1, 2)]





####  czy dany uzytkownik istnieje w bazie?
####is_user_in_bd = any(user[0] =='uuu' for user in users)
##uzytkownik = 'bambik'
##print(f"\nW bazie istnieje użytkownik {uzytkownik}? ",any(user[0] == uzytkownik for user in users),'\n')
##




#  change user's password
@connect
def change_status(username, status):
    query = f"UPDATE users SET active = %s WHERE username = %s RETURNING id"
    values = (status, username,)
    return query, values

##print(change_status('ola', True))


##
#####         wydruk słownika otrzymanego jako rezultat z bazy, po zapytaniu:
#####         cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
####for row in users:
####    print("--------")
####    for key, value in row.items():
####        print(f"{key}: {value}")
##



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
##
#print("Inserted message_id: ", new_message('lala', 'beata', 'info od lala do beata'), "\n")
##



# messages TO user
@connect
def select_messages_to(name):
    query = f'''SELECT m.id, u1.username, u2.username, m.content, created_at
FROM messages m JOIN users u1 ON m.from_id = u1.id
JOIN users u2 ON m.to_id = u2.id
WHERE u2.username = %s '''
    values = (name, )
    return query, values

##aa = select_messages_to('beata')
##print(aa)



# messages FROM user
@connect
def select_messages_from(name):
    query = f'''SELECT m.id, u1.username, u2.username, m.content, created_at
FROM messages m JOIN users u1 ON m.from_id = u1.id
JOIN users u2 ON m.to_id = u2.id
WHERE u1.username = %s '''
    values = (name, )
    return query, values

##ff = select_messages_from('zuzia')
##print(f'wiadomości od ...... \n{ff}')




##
##### zamiana wyniku zapytania o wiadomosci do bazy na format słownika
def databese_result_to_dict(db_result):
    dictionary = {}
    for row in db_result:
        #row = row[0][1:-1].split(",")
        dictionary[row[0]] = {'from' : row[1],
                            'to' : row[2],
                            'content' : row[3].strip('"'),
                            'datetime' : row[4].strftime("%d.%m.%Y %H:%M:%S"),#.strip('"'),
                            }
    return dictionary

##
##bb = databese_result_to_dict(aa)
##print(bb)


# number of not read messages to user
@connect
def nbr_of_unread_msgs(name):
    query =f'''SELECT COUNT (*)
FROM messages m JOIN users u ON m.to_id = u.id
WHERE m.read = false AND u.username = %s '''
    values = (name, )
    return query, values



##cc = nbr_of_unread_msgs('lala')
##print(cc[0][0])



#  set message status read - true
@connect
def mark_msg_read(msg_id):
    query = f"UPDATE messages SET read = true WHERE id = %s RETURNING id"
    values = (msg_id, )
    return query, values


#print(mark_msg_read(4))
##
##if __name__ == "__main__":
##    print("Hello, World!")


