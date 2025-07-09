import mysql.connector
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to open MySQL connection and close after function call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Juniorboy58*',
            database='ALX_prodev'
        )
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# Example usage:
users = fetch_users_with_cache(query="SELECT * FROM user_data")
users_again = fetch_users_with_cache(query="SELECT * FROM user_data")  # should use cache

