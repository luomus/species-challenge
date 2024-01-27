# Common database functions.

import mysql.connector
from contextlib import contextmanager
import os

@contextmanager
def connection():
    """
    Context manager for creating and managing a database connection using environment variables for configuration.

    Yields:
        MySQLConnection: The database connection object.
    """
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

def select(conn, query, params = None):
    """
    Executes a SELECT query and returns the results as a list of dictionaries.

    Args:
        conn (MySQLConnection): The database connection object.
        query (str): The SELECT query to be executed.
        params (tuple, optional): Parameters to be used in the query. Defaults to None.

    Returns:
        list of dict: The query results, with each row represented as a dictionary.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        # Use column names as dictionary keys 
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()

def transaction(conn, query, params):
    """
    Executes an transaction (INSERT or UPDATE) and commits it.

    Args:
        conn (MySQLConnection): The database connection object.
        query (str): The query to be executed.
        params (tuple): Parameters to be used in the query.

    Returns:
        bool: True if the query was successfully executed and committed, False otherwise.
        int: The ID of the last inserted row, if any.
    """
    print(query)
    print(params)

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        return True, last_id
    except Exception as e:
        conn.rollback()
        return False, None
    finally:
        cursor.close()

