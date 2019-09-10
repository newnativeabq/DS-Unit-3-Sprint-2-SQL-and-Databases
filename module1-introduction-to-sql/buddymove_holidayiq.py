'''
Module 1 Part 2: PANDAS to sql and queries
'''
import sqlite3
import pandas as pd
import os

# Create database
database_name = 'buddymove_holidayiq.sqlite3'
connection = sqlite3.connect('buddymove_holidayiq.sqlite3')

csv_data = 'buddymove_holidayiq.csv'
df = pd.read_csv(csv_data)

try:
    df.to_sql(name='buddydata', con=connection, index=False)

except ValueError as e:
    print(e, ' Continuing with program')

# Verify Data in db
cursor = connection.cursor()
query = "SELECT * FROM buddydata LIMIT 10"
cursor.execute(query)
assert cursor.fetchall() is not None


# Count Rows
query = "SELECT COUNT('User Id') FROM buddydata"
cursor.execute(query)
row_count = list(cursor.fetchall())[0][0]
print(row_count, 'Rows')

# Greater than 100 nature and greater than 100 shopping
query = "SELECT COUNT('User Id') FROM buddydata \
            WHERE Nature > 100 AND Shopping > 100"
cursor.execute(query)
row_count = list(cursor.fetchall())[0][0]
print(row_count, 'Number of people >100 Nature, >100 Shopping')

# Delete database(clean folder):
connection.close()
os.remove(database_name)