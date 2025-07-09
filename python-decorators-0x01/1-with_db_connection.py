#!/usr/bin/python3
import sqlite3
import functools


def with_db_connection(func):
    """Decorator to open and close a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a user by ID using the provided connection."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)

