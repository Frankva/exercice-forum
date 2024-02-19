import sys
from pool import get_connection

def get_request_insert():
    '''
    >>> type(get_request_insert())
    <class 'str'>
    '''
    return ('INSERT messages (text, person_id) '
        + 'VALUES '
        + '(?, ?); ')

def get_request_message_answer_question():
    '''
    >>> type(get_request_message_answer_question())
    <class 'str'>
    '''
    return ('INSERT message_answer_question (message_id, question_id) '
        'VALUES '
        '((SELECT max(message_id) '
        '    FROM messages), ?); ')

def insert(text, person_id, question_id):
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




if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
