import sys
from pool import get_connection

def get_request_select():
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT name '
        'FROM authorization_groups '
        'NATURAL JOIN person_belong_group '
        'WHERE person_id=?; ')

def select(person_id: int) -> str:
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select(), (person_id, ))
        rows = tuple(map(lambda row: {'name': row[0] }, cur))
        return rows['name']
    except Exception as e:
        print(e)
    finally:
        conn.close()

def is_admin(person_id: int) -> bool:
    '''
    >>> type(is_admin(1))
    >>> print(is_admin(1))
    <class 'bool'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select(), (person_id, ))
        rows = tuple(map(lambda row: {'name': row[0] }, cur))
        return bool(rows[0]['name'])
    except Exception as e:
        print(e)
    finally:
        conn.close()


    
if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
