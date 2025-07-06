import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root', 
        password='Juniorboy58*',
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

# Make the function accessible when the module is imported using __import__
stream_users = stream_users

