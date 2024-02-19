# Module Imports
import mariadb
import sys
import json

def get_config():
    '''
    >>> type(get_config())
    <class 'dict'>
    '''
    f = open("config.json", "r")
    text = f.read()
    f.close()
    return json.loads(text)


# Connect to MariaDB Platform
def get_connection(test=False):
    '''
    >>> type(get_connection())
    <class 'mariadb.connections.Connection'>
    '''
    try:
        db = get_config()['db'] if not test else get_config()['dbtest']
        conn = mariadb.connect(
            user=db['user'],
            password=db['password'],
            host=db['host'],
            port=db['port'],
            database=db['database']
        )
        conn.autocommit = False
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def get_connection_test():
    '''
    >>> type(get_connection_test())
    <class 'mariadb.connections.Connection'>
    '''
    return get_connection(True)


# Get Cursor
# cur = conn.cursor()
# 
# cur.execute("SELECT * FROM people")
# a = cur.fetchone()
# conn.close()
# print(a)
# print(type(a))
if __name__ == "__main__":
    import doctest
    doctest.testmod()
