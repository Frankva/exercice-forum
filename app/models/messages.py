import sys
from pool import get_connection

def get_request_select_person_messages() -> str:
    '''
    >>> type(get_request_select_person_messages())
    <class 'str'>
    '''
    return ('SELECT message_id, text, create_date '
        'FROM messages '
        'NATURAL JOIN people '
        'WHERE person_id=? '
        'ORDER BY create_date DESC; ')

def select_person_messages(person_id: int) -> tuple: 
    '''
    >>> type(select_person_messages(1))
    <class 'tuple'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select_person_messages(), (person_id, ))
        rows = tuple(map(lambda row: {'message_id': row[0], 'text': row[1],
                                      'create_date': row[2]}, cur))
        return rows
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_request_nullify_message() -> str:
    '''
    >>> type(get_request_nullify_message())
    <class 'str'>
    '''
    return ('UPDATE messages SET text = NULL '
        'WHERE message_id = ?; ')

def nullify_message(message_id: int) -> None:
    '''
    >>> type(nullify_message(2))
    <class 'NoneType'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_nullify_message(), (message_id, ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
