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

            postgres_query , values = func()
##            record = func(cursor, connection)

            cursor.execute(postgres_query, values)
            connection.commit()

            try:
                record = cursor.fetchall()
                #print("Selected names: ", record, "\n")
            except:
                print("Nothing to fetch")

                
            print("Query executed successfully")

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

@connect
def func(): #(cursor, connection):
    tab = 'account'
##    postgres_query = f'''
##                        SELECT username FROM {tab}
##                      '''
    dat = datetime.datetime.now()
    print(type(dat))
    print(dat)
    postgres_query = "INSERT INTO account (username, password, name, created_on) VALUES (%s, %s, %s, %s) RETURNING user_id;"          
    values = ('rewq2000', 'www2000', 'test2000', datetime.datetime.now())              

##    cursor.execute(postgres_query)
##    connection.commit()
##    record = cursor.fetchall()
##    return record
    return postgres_query, values
##    postgres_query = f"INSERT INTO {tab} (username, password, name, created_on) VALUES ({a}, {b}, {c}, {d})"
                    #, 'www200', 'test200', datetime.datetime.now()) '''
                    #% ('rewq200', 'www200', 'test200', datetime.datetime.now())
####
####        

    


#print("Selected names: ", record, "\n")
print("Inserted user_id: ", func()[0], "\n")
#print(func())

# Do INSERT dodac w zaptaniu opcje RETURN ..... (tu podac co ma zwracac po wstawieniu do tabeli)

##print(f'''INSERT INTO AAAAAAA (
##        username, password, name, created_on)
##        VALUES(%s, %s, %s, %s) ''' % ('rewq200', 'www200', 'test200', datetime.datetime.now()))
##




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


