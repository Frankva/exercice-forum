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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
