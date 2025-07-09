# Python Decorators - ALX Backend

## Project: `python-decorators-0x01`

This project focuses on the use of **Python decorators** to improve database interaction and write reusable, clean, and efficient code.
You will use decorators to log SQL queries, manage database connections and transactions, implement retries for failed queries, and cache query results.

---

## 📚 Learning Objectives

By completing this project, I have learned to:

- Understand and implement Python decorators.
- Apply decorators to handle database operations dynamically.
- Manage transactions with commit/rollback functionality.
- Improve performance with result caching.
- Add resilience to database queries with retry mechanisms.
- Eliminate repetitive code with reusable logic.

---

## 📁 Project Structure

```bash
python-decorators-0x01/
├── 0-log_queries.py            # Logs SQL queries before execution
├── 1-handle_connection.py      # Decorator for managing database connections
├── 2-transaction.py            # Decorator for handling transactions
├── 3-retry.py                  # Retry failed database queries
├── 4-cache_query.py            # Cache the result of queries
├── users.db                    # SQLite3 test database
├── init_db.py                  # Script to create the database and insert test users
├── README.md                   # Project documentation

