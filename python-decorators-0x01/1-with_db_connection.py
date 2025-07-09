#!/usr/bin/python3
import mysql.connector
import functools

def with_db_connection(func):
    """Decorator to handle DB connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Juniorboy58*",
            database="ALX_prodev"
        )
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

# Main test
if __name__ == "__main__":
    test_id = "0076fa94-80e9-4c28-9c7b-4cdd1557e7fc" 
    user = get_user_by_id(user_id=test_id)
    print(user)

