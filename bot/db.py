from config import CONFIG
import mysql.connector as mysql

def get_dbh():
    return mysql.connect(
        user        = CONFIG['DBUSER'],
        password    = CONFIG['DBPASS'],
        database    = CONFIG['DBNAME'],
    )

# return results list of dicts
def select(cur, sql, args=(), one=False, null_as_blank=True):
    cur.execute(sql, args)
    rv  = []
    for row in cur:
        if null_as_blank:
            row = [ '' if x is None else x for x in row ]
        cols = tuple([x[0] for x in cur.description])
        rv.append(dict(zip(cols, row)))

    return (rv[0] if rv else None) if one else rv

def select_one(cur, sql, args=()):
    return select(cur, sql, args, one=True)
