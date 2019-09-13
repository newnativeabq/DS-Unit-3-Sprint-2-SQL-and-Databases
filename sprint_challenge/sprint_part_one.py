'''
Sprint Challenge: Unit 3
SQL And Database Technologies Review
'''

import sqlite3

# Helper Functions

def make_sqlite_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connection to: ', db_file, ' successful')
    except Error as e:
        print(e)
    return conn

def execute_commit_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.commit()

def create_sqlite_table(connection, table_name, columns_detail):
    '''
    Generate SQlite table at connection with basic parameters.
    Constraints not implemented

    Parameters
    ------------------------------------
    connection: sqlite3 connection object
    table_name: string-like object
    columns: tuple-like object (column_name, type)
    '''

    columns_string = []
    for column_info in columns_detail:
        columns_string.append(' '.join(column_info))
    columns_string = ','.join(columns_string)

    query = "CREATE TABLE {} ({})".format(table_name, columns_string)
    # Database lock error - DEBUG concurrancy isue on SMB shares.
    execute_commit_query(connection=connection, query=query)

def insert_data_sqlite(connection, table_name, dict_of_values):
    column_str = []
    value_str = []
    for key, val in dict_of_values.items():
        column_str.append(str(key))
        value_str.append("'"+str(val)+"'")
    column_str = ','.join(column_str)
    value_str = ','.join(value_str)
    query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, column_str, value_str)
    print(query)
    execute_commit_query(connection, query)

# Part 1A - Making and Populating a Database

demo_conn = make_sqlite_connection('demo_data.sqlite3')

create_sqlite_table( # Does not check if table exists.  Will conflict if run twice
    connection=demo_conn,
    table_name='demo',
    columns_detail=[
        ('s', 'VARCHAR PRIMARY KEY'),
        ('x', 'INT'),
        ('y', 'INT'),
    ]
    )

data_to_insert = {
    's': ['g','v','f'],
    'x': [3,5,8],
    'y': [9,7,7],
    }

for i in range(len(data_to_insert['s'])):
    s = data_to_insert['s'][i]
    x = data_to_insert['x'][i]
    y = data_to_insert['y'][i]
    insert_data_sqlite(
        connection=demo_conn,
        table_name='demo',
        dict_of_values={'s':s, 'x':x, 'y':y}
    )

demo_conn.close()