# ??????????????????????????

import psycopg2, time, datetime
from configparser import ConfigParser
import bcrypt
#from psycopg2 import extras

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
            print('Connecting to the PostgreSQL database...')
            connection = psycopg2.connect(**db_parameters)

            # Create a cursor to perform database operations
            cursor = connection.cursor()

            # kursor - wynik zapytania jest slownikiem
            #cursor = connection.cursor(cursor_factory=extras.RealDictCursor)


            #print("PostgreSQL server information")
            #print(connection.get_dsn_parameters(),'\n')

            postgres_query , values = func(*args, **kwargs)
##            record = func(cursor, connection)

            cursor.execute(postgres_query, values)
            connection.commit()
 
##            columns = list(cursor.description)
##            print(columns[0][0])
            try:
                record = cursor.fetchall()
                #print("Selected names: ", record, "\n")
            except:
                print("Nothing to fetch")

                
            print(f"Query {func.__name__} executed successfully")

        except (Exception, psycopg2.Error) as error:
             print("Error while connecting to PostgreSQL:\n",error)

##        except:
##            print("Error while connecting to PostgreSQL")
        finally:
            if connection:  # czy taki warunek jest OK?
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")  
        
        return record
    return wrapper


def hash_pswrd(pswrd):
    salt = bcrypt.gensalt()
    print(salt)
    return bcrypt.hashpw(pswrd.encode(), salt)

aa=hash_pswrd('MAMA')
print(aa)
print(bcrypt.checkpw(b'MAMA', aa))

bb=hash_pswrd('MAMA')
print(bb)
print(bcrypt.checkpw('MAMA'.encode(), bb))

cc=hash_pswrd('iuyt')
print(cc)
print(bcrypt.checkpw('iuyt'.encode(), cc))





####  Nowy użytkownik - do bazy
@connect
def insert_new_account(username, name, passw, role = 2): #(cursor, connection):
    postgres_query = f'''INSERT INTO users (username, password, name, created_on)
VALUES (%s, %s, %s, %s) RETURNING id'''          
    values = (username, name, passw, datetime.datetime.now())              
    return postgres_query, values

##print("Inserted user_id: ", insert_new_account('beata', 'haslo beaty', 'name beata'), "\n")
##

##  lista uzytkowników z bazy,
## lista z WIDOKU active_users (uzytkownicy o statusie True)
@connect
def select_active_users():
    postgres_query = f"SELECT username FROM active_users"
    values = ()
    return postgres_query, values

usersA = select_active_users()  # 't' - True, 'f' - False

print("Selected names: ", usersA)

## wszyscy użytkownicy istniejący w bazie
@connect
def select_users():
    postgres_query = f"SELECT username FROM users"
    values = ()
    return postgres_query, values

users = select_users()  # 't' - True, 'f' - False

print("Selected names: ", users)



##### ZMIANA hasła  OK
@connect
def change_pswrd(pswrd, username):
    query = f"UPDATE users SET password = %s WHERE username = %s RETURNING id"
    values = (pswrd, username,)
    return query, values
##
##print(change_pswrd('Nowe haselko-10 oli', 'ola'))


##### ZMIANA statusu uzytkownika (aktywny true/false)  OK
@connect
def change_status(username, status):
    query = f"UPDATE users SET active = %s WHERE username = %s RETURNING id"
    values = (status, username,)
    return query, values
##

##print(change_status('ola', True))



####  czy dany uzytkownik istnieje w bazie?
##is_user_in_bd = any(user[0] =='uuu' for user in users)
##print("W bazie istnieje użytkownik 'uuu'? ",any(user[0] =='uuu' for user in users))
##
##
#####         wydruk słownika otrzymanego jako rezultat z bazy, po zapytaniu:
#####         cursor = connection.cursor(cursor_factory=extras.RealDictCursor)
####for row in users:
####    print("--------")
####    for key, value in row.items():
####        print(f"{key}: {value}")
##
##
##
###  !! OK !!
###  Nowa wiadomosc do bazy danych
##@connect
##def new_message(sender, recipient, content):
##    query = f'''INSERT INTO messages (from_id, to_id, content)
##VALUES ( 
##(SELECT id FROM users WHERE username = %(sender)s),
##(SELECT id FROM users WHERE username = %(recipient)s), 
##%(content)s)
##RETURNING id'''          
##    values = ({'sender' : sender, 'recipient' :recipient, 'content' :content})              
##    return query, values
##
##print("Inserted message_id: ", new_message('zuzia', 'ola', 'info od zuzia do ola'), "\n")
##


##
##
##
### wybierz wiadomosc DO zadanego użytkownika
@connect
def select_messages_to(name):
    query = f'''SELECT m.id, u1.username, u2.username, m.content, created_at
FROM messages m JOIN active_users u1 ON m.from_id = u1.id
JOIN active_users u2 ON m.to_id = u2.id
WHERE u2.username = %s '''
    values = (name, )
    return query, values

aa = select_messages_to('ola')
print(aa)
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
bb = databese_result_to_dict(aa)
print(bb)

##
##### ustaw status wiadomości o id = msg_id na "przeczytana" 
##@connect
##def mark_msg_read(msg_id):
##    query = f"UPDATE message SET read = True WHERE message_id = %s RETURNING message_id"
##    values = (msg_id, )
##    return query, values
##
##
##print(mark_msg_read(18))
##
##   
##

##
##### ZEBRANIE W JEDNĄ FUNKCJE ### CZY MA SENS ???
##
##querys = {'select_names' : f"SELECT username FROM account",
##          'select_messages_to': f'''SELECT (message_id, sender, recipient, content, created_time)
##FROM message WHERE recipient = %s ''',
##          'new_message' : f'''INSERT INTO message (sender, recipient, content, created_time)
##VALUES (%s, %s, %s, %s) RETURNING message_id''',
##          }
##
##
##@connect
##def query(query, *args):
##    values = (args,)
##    return query, values
##
###print(query(querys['select_messages_to'], "to"))
###print(query(querys['select_names']))
##print(query(querys['new_message'],('nada', 'odbioe', 'takka se wiadomosc', datetime.datetime.now())))
##

