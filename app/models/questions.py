import sys
from pool import get_connection
import tags as tagsModel
from functools import reduce
from votes import get_vote_on_question, get_uservote_on_question, get_vote

def get_request_insert1() -> str:
    '''
    >>> type(get_request_insert1())
    <class 'str'>
    '''
    return ('INSERT INTO questions (title) '
       'VALUES '
       '(?); ')

def get_request_insert2() -> str:
    '''
    >>> type(get_request_insert2())
    <class 'str'>
    '''
    return('INSERT INTO messages (text, person_id) '
       'VALUES '
       '(?, ?); ')

def get_request_insert3() -> str:
    '''
    >>> type(get_request_insert3())
    <class 'str'>
    '''
    return ('INSERT INTO question_have_message (question_id, message_id) '
       'VALUES '
       '((SELECT MAX(question_id) FROM questions), '
       '    (SELECT MAX(message_id) FROM messages)); ')

def get_request_insert4() -> str:
    '''
    >>> type(get_request_insert4())
    <class 'str'>
    '''
    return ('INSERT INTO question_have_tag (question_id, tag_id) '
        'VALUES '
        '((SELECT MAX(question_id) FROM questions),  '
        '        (SELECT tag_id FROM tags WHERE name=?)); ')


def get_request_select() -> str:
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT question_id, title '
        'FROM questions '
        'ORDER BY question_id DESC; ')

def insert(title: str, body: str, tags: tuple, user_id) -> None:
    '''
    >>> type(insert('titre question', 'corps message', ('tag1', 'tag2'), 1))
    <class 'NoneType'>
    '''
    try: 
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_insert1(), (title, ))
        cur.execute(get_request_insert2(), (body, user_id))
        cur.execute(get_request_insert3())
        def f(tag):
            cur.execute(tagsModel.get_request_select(), (tag, ))
            return tag, cur.fetchone()
        tags_with_id = tuple(map(f, tags))
        tags_to_insert = tuple(filter(
            lambda tag: tag[1] is None, tags_with_id))
        for tag, _ in tags_to_insert:
            cur.execute(tagsModel.get_request_insert(), (tag, ))
        for tag in tags:
            cur.execute(get_request_insert4(), (tag, ))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()


def select_no_commit(conn):
    '''
    >>> type(select_no_commit(get_connection()))
    <class 'tuple'>
    '''
    cur = conn.cursor()
    cur.execute(get_request_select())
    rows = tuple(map(lambda row: {'question_id': row[0],
                                  'title': row[1]}, cur))
    return rows


def select() -> tuple:
    '''
    >>> type(select())
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        return select_no_commit(conn)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_request_select_with_message_id() -> str:
    '''
    >>> type(get_request_select_with_message_id())
    <class 'str'>
    '''
    return ('SELECT question_id, title, message_id '
        'FROM questions '
        'NATURAL JOIN question_have_message; ')

def select_order_by_vote() -> tuple:
    '''
    >>> type(select_order_by_vote())
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select_with_message_id())
        rows = tuple(map(lambda row: {'question_id': row[0],
                                      'title': row[1],
                                      'message_id': row[2]}, cur))
        def f(row: dict) -> dict:
            row['vote'] = get_vote(conn, row['message_id'])
            return row
        rows_with_vote = tuple(map(f, rows))
        sorted_rows_with_vote = tuple(reversed(sorted(
            rows_with_vote, key=lambda row: row['vote'])))
        return sorted_rows_with_vote
    except Exception as e:
        print(e)
    finally:
        conn.close()


def get_request_select_one():
    '''
    >>> type(get_request_select_one())
    <class 'str'>
    '''
    return ('SELECT title, text, firstname, lastname, create_date, message_id '
        'FROM questions '
        'NATURAL JOIN people '
        'NATURAL JOIN question_have_message '
        'NATURAL JOIN messages '
        'WHERE question_id=?; ')

def select_one(question_id: int , person_id=None) -> tuple:
    '''
    >>> type(select_one(1))
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select_one(), (question_id, ))
        rows = tuple(map(lambda row: { 'title': row[0], 'text': row[1],
            'firstname': row[2], 'lastname': row[3], 'create_date': row[4],
            'message_id': row[5] }, cur))
        question = rows[0]
        cur.execute(tagsModel.get_request_select_where_question(),
                    (question_id, ))
        tags = tuple(map(lambda row: row[0], cur))
        vote = get_vote_on_question(conn, question_id)
        if person_id is None:
            return question, tags, vote, None
        uservote = get_uservote_on_question(conn, question_id, person_id)
        return question, tags, vote, uservote
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_request_select_where_tag() -> str:
    '''
    >>> type(get_request_select_where_tag())
    <class 'str'>
    '''

    return ('SELECT question_id, title '
        'FROM questions '
        'NATURAL JOIN question_have_tag '
        'NATURAL JOIN tags '
        'WHERE name=?; ')

def select_where_tag(tag) -> tuple:
    '''
    >>> type(select_where_tag('tag_name'))
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select_where_tag(), (tag, ))
        rows = tuple(map(lambda row: {'question_id': row[0],
                                             'title': row[1]}, cur))
        return rows
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
