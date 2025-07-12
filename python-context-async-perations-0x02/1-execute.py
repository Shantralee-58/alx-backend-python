import mysql.connector

class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Juniorboy58*',
            database='ALX_prodev'
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

# Usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    with ExecuteQuery(query, (25,)) as result:
        for row in result:
            print(row)

