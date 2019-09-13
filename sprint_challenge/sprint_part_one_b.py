import sqlite3


connection = sqlite3.connect('demo_data.sqlite3')

# Helper Functions
def execute_fetchall_sqlite_query(connection, query):
    cursor = connection.cursor()
    return cursor.execute(query).fetchall()

# Part 1B: Queries

## Count how many rows you have - it should be 3!
query = "SELECT COUNT(*) FROM demo"
print(query, execute_fetchall_sqlite_query(connection, query))

## How many rows are there where both x and y are at least 5?
query = "SELECT COUNT(*) FROM demo WHERE x>=5 AND y>=5"
print(query, execute_fetchall_sqlite_query(connection, query))

## How many unique values of y are there (hint - COUNT() can accept a keyword DISTINCT)?
query = "SELECT COUNT (DISTINCT y) FROM demo"
print(query, execute_fetchall_sqlite_query(connection, query))