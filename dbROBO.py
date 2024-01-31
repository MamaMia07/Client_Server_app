# ??????????????????????????

import psycopg2, time, datetime
from configparser import ConfigParser


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
            #print("PostgreSQL server information")
           # print(connection.get_dsn_parameters(),'\n')

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



#!!!!!!!!!!!  "Dictionary-like cursor", part of psycopg2.extras !!!!!!!!!!!!!



@connect
def insert_new_account(username, name, passw): #(cursor, connection):
    tab = 'account'
    postgres_query = f'''INSERT INTO {tab} (username, password, name, created_on)
VALUES (%s, %s, %s, %s) RETURNING user_id'''          
    values = (username, name, passw, datetime.datetime.now())              
    return postgres_query, values


#print("Inserted user_id: ", insert_new_account('lala', 'olla', 'haselko'), "\n")


@connect
def select_users():
    tab = 'account'
    postgres_query = f"SELECT username FROM {tab}"
    values = None
    return postgres_query, values


users = select_users()
print("Selected names: ", users)
#print("W bazie istnieje użytkownik 'lala'? ",any(user[0] =='lala' for user in users))



@connect
def new_message(sender, recipient, content):
    tab = 'message'
    query = f'''INSERT INTO {tab} (sender, recipient, content, created_time)
VALUES (%s, %s, %s, %s) RETURNING message_id'''          
    values = (sender, recipient, content, datetime.datetime.now())              
    return query, values

#print("Inserted message_id: ", new_message('from', 'to', '3. message new message'), "\n")



@connect
def select_messages_to(name):
    query = f"SELECT (message_id, sender, recipient, content, created_time) FROM message WHERE recipient = %s "
    values = (name, )
    return query, values

print(select_messages_to('to'))



@connect
def mark_msg_read(msg_id):
    query = f"UPDATE message SET read = True WHERE message_id = %s "
    values = (msg_id, )
    return query, values

print(mark_msg_read(1))

    
## # polaczenie z baza i wykonanie operacji.
##def connect():
##    try:
##        # read connection parameters
##        db_parameters = config()
##
##        # connect to the PostgreSQL server
##        print('Connecting to the PostgreSQL database...')
##        connection = psycopg2.connect(**db_parameters)
##
##        # Create a cursor to perform database operations
##        cursor = connection.cursor()
##        print("PostgreSQL server information")
##        print(connection.get_dsn_parameters(),'\n')
##
##        # Executing a SQL query
##        #cursor.execute("SELECT version();")
##        tab = 'account'
####        postgres_insert_querry = f'''
####                        INSERT INTO {tab} (
####                        username, password, name, created_on)
####                        VALUES(%s,%s,%s,%s) '''
####
####        record_to_insert = ('rewqe', 'www', 'test2', datetime.datetime.now())
####
####        cursor.execute(postgres_insert_querry, record_to_insert)
##        postgres_select_querry = f'''
##                        SELECT username FROM {tab} 
##                        '''
##
##        #record_to_insert = ('rewqe', 'www', 'test2', datetime.datetime.now())
##
##        cursor.execute(postgres_select_querry)
##
##
##
##        connection.commit()
##        # Fetch result
##        record = cursor.fetchall()
##        print("Selected names: ", record, "\n")
##        
##    except:# (Exception, psycopg2.Error):
##        print("Error while connecting to PostgreSQL")
##    finally:
##        if (connection):
##            cursor.close()
##            connection.close()
##            print("PostgreSQL connection is closed")  


