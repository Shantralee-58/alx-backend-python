# Python Context Managers and Asynchronous Programming

This project demonstrates the use of Python context managers and asynchronous programming for efficient database interactions.

## 📌 Tasks

### ✅ Task 0: `DatabaseConnection`
- Class-based context manager using `__enter__` and `__exit__` for managing SQLite DB connections.

### ✅ Task 1: `ExecuteQuery`
- Reusable context manager that executes parameterized queries.

### ✅ Task 2: `Asyncio + aiosqlite`
- Async functions `async_fetch_users` and `async_fetch_older_users` run concurrently using `asyncio.gather()`.

## 💻 Requirements

- Python 3.8+
- SQLite3
- `aiosqlite` (install with `pip install aiosqlite`)

## ⚙️ How to Run

```bash
python 0-databaseconnection.py
python 1-execute.py
python 3-concurrent.py

