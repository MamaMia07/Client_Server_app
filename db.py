import psycopg2

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
    except:# (Exception, psycopg2.Error):
        print("Error while connecting to PostgreSQL")
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")  

connect()
