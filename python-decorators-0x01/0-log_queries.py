#!/usr/bin/python3
import sqlite3
import functools
from datetime import datetime  # Required for timestamp logging


def log_queries(func):
    """Decorator to log SQL queries with timestamp before execution."""
    @functools.wraps(func)
    def wrapper(query):
        print(f"[{datetime.now()}] Executing SQL: {query}")
        return func(query)
    return wrapper


@log_queries
def fetch_all_users(query):
    """Fetch all users from the users database using the given SQL query."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users")
    for user in users:
        print(user)

