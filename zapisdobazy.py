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



 # polaczenie z baza i wykonanie operacji.
def connect():
    try:
        # read connection parameters
        db_parameters = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**db_parameters)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(),'\n')

        # Executing a SQL query
        #cursor.execute("SELECT version();")
        tab = 'account'
        postgres_insert_querry = f'''
                        INSERT INTO {tab} (
                        username, password, name, created_on)
                        VALUES(%s,%s,%s,%s) ''' 

        record_to_insert = ('rewq500', 'www500', 'test500', datetime.datetime.now())

        cursor.execute(postgres_insert_querry, record_to_insert)
        

        postgres_select_querry = f'''
                        SELECT username FROM {tab} 
                        '''
        cursor.execute(postgres_select_querry)



        connection.commit()
        # Fetch result
        record = cursor.fetchall()
        print("Selected names: ", record, "\n")
        
    except:# (Exception, psycopg2.Error):
        print("Error while connecting to PostgreSQL")
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")  
connect()

