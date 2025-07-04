""" Project: python-generators-0x00
    Author: Idah Lindiwe Khumalo

    Handles DB creation and seeding"""

import mysql.connector
import csv

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
    ''')
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            ''', (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
