# Python Generators Project

## 📌 Overview
This project explores **advanced Python programming** concepts—specifically **generators**—to process large datasets efficiently. It simulates real-world scenarios such as streaming database rows, batch processing, lazy pagination, and memory-efficient aggregations using a MySQL database.

You’ll practice using the `yield` keyword to build scalable and performant Python applications, particularly for data-intensive back-end systems.

---

## 🎯 Learning Objectives

- Understand and implement generator functions in Python.
- Efficiently stream large datasets from a MySQL database.
- Process data in batches to reduce memory usage.
- Simulate pagination using lazy evaluation.
- Perform memory-efficient aggregation without SQL aggregation functions.
- Apply clean, modular design and use proper DB connections.

---

## 🧰 Setup

### Requirements:
- Python 3.x
- MySQL Server
- `mysql-connector-python` package (`pip install mysql-connector-python`)

### Initial Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/alx-backend-python.git
   cd alx-backend-python/python-generators-0x00
   ```

2. Seed the database:
   ```bash
   python3 0-main.py
   ```

---

## 📂 Project Structure

| File                      | Description                                  |
|---------------------------|----------------------------------------------|
| `seed.py`                 | Creates database `ALX_prodev` and seeds data |
| `0-stream_users.py`       | Streams users one row at a time              |
| `1-batch_processing.py`   | Processes users in batches                   |
| `2-lazy_paginate.py`      | Implements lazy pagination of data           |
| `4-stream_ages.py`        | Calculates average age using a generator     |
| `user_data.csv`           | Sample dataset used for seeding              |

---

## ✅ Task Summaries

### Task 0: Setting up the DB
- Creates `ALX_prodev` database.
- Defines and seeds `user_data` table using CSV.
- Functions:
  - `connect_db()`
  - `create_database()`
  - `connect_to_prodev()`
  - `create_table()`
  - `insert_data()`

### Task 1: Stream Rows with a Generator
- Uses `yield` to return user records one-by-one.
- File: `0-stream_users.py`

### Task 2: Batch Processing
- Streams data in batches.
- Filters users over age 25.
- File: `1-batch_processing.py`

### Task 3: Lazy Pagination
- Fetches pages only when needed.
- Includes helper: `paginate_users(page_size, offset)`
- File: `2-lazy_paginate.py`

### Task 4: Average Age Calculation
- Uses generator to compute the average age of users without `AVG()`.
- File: `4-stream_ages.py`

---

## ▶️ Usage

To test individual modules:
```bash
python3 1-main.py    # Streams 6 users
python3 2-main.py    # Batches and filters users
python3 3-main.py    # Lazy pagination
python3 4-stream_ages.py   # Compute average age
```

---

## 🧑‍💻 Author
**Idah Lindiwe Khumalo**  
*ALX Backend Python Project - Generator Track*  
GitHub: [@Shantralee-58](https://github.com/Shantralee-58)

