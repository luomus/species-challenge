import mysql.connector
from contextlib import contextmanager
import os

@contextmanager
def connection():
    database = os.environ.get("MYSQL_DATABASE")
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = "db"
    port = 3306
    conn = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database)
    try:
        yield conn
    finally:
        conn.close()

def select(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def insert(conn, query, params):
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

