import sys
from pool import get_connection
import tags as tagsModel

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

def get_request_select() -> str:
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT question_id, title '
        'FROM questions; ')

def select() -> tuple:
    '''
    >>> type(select())
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select())
        rows = tuple(map(lambda row: {'question_id': row[0],
                                             'title': row[1]}, cur))
        return rows
    except Exception as e:
        print(e)
    finally:
        conn.close()

def get_request_select_one():
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT title, text '
        'FROM questions '
        'NATURAL JOIN question_have_message '
        'NATURAL JOIN messages '
        'WHERE question_id=?; ')

def select_one(id) -> tuple:
    '''
    >>> type(select_one(1))
    <class 'tuple'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_select_one(), (id, ))
        rows = tuple(map(lambda row: {'title': row[0],
                                             'text': row[1]}, cur))
        return rows
    except Exception as e:
        print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
