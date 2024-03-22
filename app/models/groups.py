import sys
from pool import get_connection

def get_request_select():
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT name '
        'FROM authorization_groups '
        'NATURAL JOIN people '
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

    
if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
