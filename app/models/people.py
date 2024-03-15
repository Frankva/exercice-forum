from pool import get_connection

def get_request_select() -> str:
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT *'
        'FROM people')

def get_users():
    '''
    >>> type(get_users())
    <class 'tuple'>
    '''
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(get_request_select())
    rows = cur.fetchone()
    conn.close()
    return rows

def get_request_check_password_email():
    '''
    >>> type(get_request_check_password_email())
    <class 'str'>
    '''
    return ('SELECT person_id '
        'FROM emails '
        'NATURAL JOIN people '
        'NATURAL JOIN passwords '
        'WHERE (text=?) AND (hash=sha2(?, 512)); ')

def get_person_id(email: str, password: str) -> int | None:
    '''
    >>> type(get_person_id('bob.morice@email.org', 'a'))
    <class 'int'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_check_password_email(), (email, password))
        rows = tuple(map(lambda row: row[0], cur))
        return rows[0]
    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()

def get_resquest_insert_password():
    '''
    >>> type(get_resquest_insert_password())
    <class 'str'>
    '''
    return ('INSERT passwords (hash, person_id) '
        'VALUES '
        '(sha2(?, 512), ( '
        '        SELECT MAX(person_id) '
        '        FROM people '
        ')); ')

def get_resquest_insert_email():
    '''
    >>> type(get_resquest_insert_email())
    <class 'str'>
    '''
    return ('INSERT emails (text, person_id) '
        'VALUES '
        '(?, ( '
        '        SELECT MAX(person_id) '
        '        FROM people '
        ')); ')

def get_resquest_insert_person():
    '''
    >>> type(get_resquest_insert_person())
    <class 'str'>
    '''
    return ('INSERT people (firstname, lastname) '
        'VALUES '
        '(?, ?); ')
    
def insert_person(firstname:str, lastname: str, email: str,
                  password: str) -> None:
    '''
    >>> type(insert_person('firstsname', 'lastname','bob.morice@email.org',
    ... 'password'))
    <class 'NoneType'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_resquest_insert_person(), (firstname, lastname))
        cur.execute(get_resquest_insert_email(), (email, ))
        cur.execute(get_resquest_insert_password(), (password, ))
        # TODO
        conn.commit()
    except Exception as e:
        print(e, file=sys.stderr)
        conn.rollback()
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
