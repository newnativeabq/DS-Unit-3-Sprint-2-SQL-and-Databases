import psycopg2

import setup
import os
import pandas as pd

setup.commit_environ_vars()

# Database Connections
def make_remote_connection():
    pg_conn = psycopg2.connect(
        dbname = os.environ.get('dbname'),
        user = os.environ.get('user'),
        password = os.environ.get('password'),
        host = os.environ.get('host'),
    )
    return pg_conn

def make_sqlite_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connection to: ', db_file, ' successful')
    except Error as e:
        print(e)

    return conn

def create_pg_table(table_name, full_query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(full_query)
        cursor.close()
        connection.commit()
    except psycopg2.ProgrammingError as e:
        print(e)

def get_titanic_val(dataframe, row_to_return):
   list_data = dataframe.iloc[row_to_return].to_list()
   for i in range(len(list_data)):
       if type(list_data[i]) == str:
           list_data[i] = "''".join(list_data[i].split("'"))
           list_data[i] = "'"+str(list_data[i])+"'"
       else:
           list_data[i] = str(list_data[i])
   return ','.join(list_data)

# Queries (titanic_data)
create_titanic_table_query = """
    CREATE TABLE titanic_dataset (
        id SERIAL PRIMARY KEY,
        survived INT,
        pclass INT,
        name VARCHAR(100),
        sex VARCHAR(10),
        age INT,
        siblings_or_spouses_aboard INT,
        parents_or_children_aboard INT,
        fare FLOAT
    );
"""
def generate_titanic_insert_query(dataframe, row):
    insert_titanic_row_query ="""
        INSERT INTO titanic_dataset
        (survived, pclass, name, sex, age, siblings_or_spouses_aboard, parents_or_children_aboard, fare)
        VALUES(""" + get_titanic_val(dataframe, row) + ');'
    return insert_titanic_row_query



if __name__ == "__main__":
    data = pd.read_csv('titanic.csv')

    # New Connections
    pg_conn = make_remote_connection()
    pg_curs = pg_conn.cursor()

    # Create Destination Table
    create_pg_table('titanic_dataset', create_titanic_table_query, pg_conn)

    # Insert into Destination Table
    print('Attempting to add ', len(data.index), 'rows')
    for i in range(len(data.index)):
        insert_query = generate_titanic_insert_query(data, i)
        print(insert_query)
        pg_curs.execute(insert_query)

    # Commit changes
    pg_curs.close()
    pg_conn.commit()
    pg_conn.close()
