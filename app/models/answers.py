import sys
from pool import get_connection
from votes import get_vote, get_uservote

def get_request_insert() -> str:
    '''
    >>> type(get_request_insert())
    <class 'str'>
    '''
    return ('INSERT messages (text, person_id) '
        'VALUES '
        '(?, ?); ')

def get_request_message_answer_question() -> str:
    '''
    >>> type(get_request_message_answer_question())
    <class 'str'>
    '''
    return ('INSERT message_answer_question (message_id, question_id) '
        'VALUES '
        '((SELECT max(message_id) '
        '    FROM messages), ?); ')

def insert(text: str, person_id: int, question_id: int) -> None:
    '''
    >>> type(insert('text', 1, 1))
    <class 'NoneType'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_insert(), (text, person_id ))
        cur.execute(get_request_message_answer_question(), (question_id, ))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

def get_request_select() -> str:
    '''
    >>> type(get_request_message_answer_question())
    <class 'str'>
    '''
    return ('SELECT message_id, text, firstname, lastname, create_date, '
        '    COALESCE(GROUP_CONCAT(name), \'\') AS \'group\' '
        'FROM messages '
        'NATURAL JOIN message_answer_question '
        'NATURAL JOIN people '
        'NATURAL LEFT JOIN person_belong_group '
        'NATURAL LEFT JOIN authorization_groups '
        'WHERE question_id=? '
        'GROUP BY message_id, text, firstname, lastname, create_date; ')

def select(question_id: int, person_id=None) -> tuple:
    '''
    >>> type(select(1))
    <class 'tuple'>
    >>> type(select(1, 1))
    <class 'tuple'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select(), (question_id, ))
        rows = tuple(map(lambda row: {'message_id': row[0], 'text': row[1],
                'firstname': row[2], 'lastname': row[3],
                'create_date': row[4], 'group': row[5]}, cur))
        def f(row: dict) -> dict:
            row['vote'] = get_vote(conn, row['message_id'])
            return row
        rows_with_vote = tuple(map(f, rows))
        sorted_rows_with_vote = tuple(reversed(sorted(rows_with_vote,
                                       key=lambda row: row['vote'])))
        if person_id is None:
            return sorted_rows_with_vote
        def f(row: dict) -> dict:
            row['uservote'] = get_uservote(conn, row['message_id'], person_id)
            return row
        rows_with_uservote = tuple(map(f, sorted_rows_with_vote))
        return rows_with_uservote
    except Exception as e:
        raise e
    finally:
        conn.close()




if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
