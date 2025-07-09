import mysql.connector
import functools

def with_db_connection(func):
    """Decorator to open a MySQL connection, pass it to func, and close after."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Juniorboy58*',
            database='ALX_prodev'
        )
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def transactional(func):
    """Decorator to wrap function inside transaction: commit or rollback."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
    cursor.close()

# Example usage:
update_user_email(user_id='some-uuid-or-id', new_email='Crawford_Cartwright@hotmail.com')

