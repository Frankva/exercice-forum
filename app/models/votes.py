
import sys

from pool import get_connection

def get_request_insert_vote() -> str:
    '''
    >>> type(get_request_insert_vote())
    <class 'str'>
    '''

    return ('INSERT person_vote_message (is_upvote, person_id, message_id) '
        'VALUES '
        '(?, ?, ?) '
        'ON DUPLICATE KEY UPDATE '
        'is_upvote=VALUES(is_upvote); ')

def insert_vote(is_upvote, person_id, message_id) -> None:
    '''
    >>> type(insert_vote(True, 1, 1))
    <class 'NoneType'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_insert_vote(),
                    (is_upvote, person_id, message_id))
        conn.commit()
    except Exception as e:
        print(e, file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

def get_request_delete_vote() -> str:
    '''
    >>> type(get_request_delete_vote())
    <class 'str'>
    '''

    return ('DELETE '
        'FROM person_vote_message '
        'WHERE (person_id=?) AND (message_id=?); ')

def delete_vote(person_id, message_id) -> None:
    '''
    >>> type(delete_vote(1, 1))
    <class 'NoneType'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_delete_vote(), (person_id, message_id))
        conn.commit()
    except Exception as e:
        print(e, file=sys.stderr)
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
