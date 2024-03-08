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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
