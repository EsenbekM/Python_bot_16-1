import psycopg2
from config import URI

db = psycopg2.connect(URI, sslmode='require')
cursor = db.cursor()

def psql_create():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, fullname TEXT);")
        db.commit()
    except:
        cursor.execute("rollback")
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, fullname TEXT);")
        db.commit()
