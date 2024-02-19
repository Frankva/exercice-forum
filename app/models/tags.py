import sys

from pool import get_connection

def get_request_insert() -> str:
    '''
    >>> type(get_request_insert())
    <class 'str'>
    '''
    return ( 'INSERT INTO tags (name) '
            'VALUES '
            '(?); ')

def get_request_select() -> str:
    '''
    >>> type(get_request_select())
    <class 'str'>
    '''
    return ('SELECT tag_id '
        'FROM tags '
        'WHERE name=?; ')

def insert(name) -> None:
    '''
    >>> type(insert('nom-du-tagw'))
    <class 'NoneType'>
    '''
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(get_request_insert(), (name, ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e, file=sys.stderr)

def formatTags(rawTags: str) -> tuple:
    '''
    >>> formatTags('a,b;c d d       a')
    ('a', 'b', 'c', 'd')
    '''
    cleanedTags = rawTags.replace(',', ' ')
    cleanedTags2 = cleanedTags.replace(';', ' ')
    tags = list(set(cleanedTags2.split()))
    tags.sort()
    return tuple(tags)



if __name__ == "__main__":
    import doctest
    from pool import get_connection_test as get_connection
    doctest.testmod()
