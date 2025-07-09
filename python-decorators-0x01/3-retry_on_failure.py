#!/usr/bin/python3
import mysql.connector
import time
import functools

# ------------------------
# Decorator: with_db_connection
# ------------------------
def with_db_connection(func):
    """Decorator to open and close MySQL DB connection automatically"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Juniorboy58*",
            database="ALX_prodev"
        )
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# ------------------------
# Decorator: retry_on_failure
# ------------------------
def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a DB operation if it fails"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[Retry {attempt}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

# ------------------------
# Your DB Operation
# ------------------------
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    return cursor.fetchall()

# ------------------------
# Main Program
# ------------------------
if __name__ == "__main__":
    users = fetch_users_with_retry()
    for user in users:
        print(user)

