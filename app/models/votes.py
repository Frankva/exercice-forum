
import sys

from pool import get_connection

from functools import reduce

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

def get_request_vote() -> str:
    '''
    >>> type(get_request_vote())
    <class 'str'>
    '''
    return ('SELECT ( '
        '    SELECT count(person_vote_message_id) '
        '    FROM person_vote_message '
        '    WHERE (is_upvote=true) AND (message_id=?) '
        ') - ( '
        '    SELECT count(person_vote_message_id) '
        '    FROM person_vote_message '
        '    WHERE (is_upvote=false) AND (message_id=?) '
        ') AS vote; ')

def get_vote(conn, message_id) -> int: 
    cur = conn.cursor()
    cur.execute(get_request_vote(), (message_id, message_id))
    vote = reduce(lambda vote, row: row[0], cur, 0)
    return vote

def get_vote_conn(message_id) -> int:
    '''
    >>> type(get_vote_conn(1))
    <class 'int'>
    '''
    try: 
        conn = get_connection()
        return get_vote(conn, message_id)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_request_user_vote() -> str:
    '''
    >>> type(get_request_user_vote())
    <class 'str'>
    '''
    return ('SELECT is_upvote '
        'FROM person_vote_message '
        'WHERE  (message_id=?) AND (person_id=?); ')

def get_uservote(conn, message_id: int, user_id: int) -> int:
    '''
    return 1 is upvote, 0 is no vote, -1 is downvote
    >>> type(get_uservote(get_connection(), 1, 1))
    <class 'int'>
    '''
    cur = conn.cursor()
    cur.execute(get_request_user_vote(), (message_id, user_id))
    vote = reduce(lambda vote, row: row[0], cur, None)
    if vote == 0:
        return -1
    if vote == 1:
        return 1
    return 0


if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
