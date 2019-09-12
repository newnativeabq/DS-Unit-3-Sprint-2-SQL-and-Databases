import sqlite3
import psycopg2

import setup
import os

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

def get_rpg_val(data, row_to_return):
    return str(data[row_to_return][1:])



# Queries (rpg_data)
create_rpg_table_query = """
    CREATE TABLE charactercreator_character (
        character_id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        level INT,
        exp INT,
        hp INT,
        strength INT,
        intelligence INT,
        dexterity INT,
        wisdom INT
    );
"""
def generate_rpg_insert_query(data, row):
    insert_rpg_row_query ="""
        INSERT INTO charactercreator_character
        (name, level, exp, hp, strength, intelligence, dexterity, wisdom)
        VALUES""" + get_rpg_val(data, row) + ';'
    return insert_rpg_row_query


if __name__ == "__main__":
    # New Connections
    pg_conn = make_remote_connection()
    pg_curs = pg_conn.cursor()

    # Create Destination Table
    create_pg_table('charactercreator_character', create_rpg_table_query, pg_conn)

    # Get Origin Data
    origin_conn = make_sqlite_connection('rpg_db.sqlite3')
    origin_curs = origin_conn.cursor()
    characters = origin_curs.execute("SELECT * FROM charactercreator_character;").fetchall()

    # Insert into Destination Table
    for i in range(len(characters)):
        insert_query = generate_rpg_insert_query(characters, i)
        print(insert_query)
        pg_curs.execute(insert_query)

    # Commit changes
    pg_curs.close()
    pg_conn.commit()