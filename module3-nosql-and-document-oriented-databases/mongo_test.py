import sqlite3
import os
import pandas as pd
import pymongo

import setup

setup.commit_environ_vars()

def make_sqlite_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connection to: ', db_file, ' successful')
    except Error as e:
        print(e)
    return conn

def table_to_dataframe(connection, table_name):
    query = "SELECT * FROM " + table_name
    return pd.read_sql(query, connection)

if __name__ == "__main__":
    client = pymongo.MongoClient(os.environ.get("clientURL"))
    db = client.rpg

    # Convert SQL Data to JSON and import into MongoDB
    connection = make_sqlite_connection('rpg_db.sqlite3')
    rpg_table_list = [
        'armory_item',
        'armory_weapon',
        'charactercreator_character',
        'charactercreator_character_inventory',
        'charactercreator_cleric',
        'charactercreator_fighter',
        'charactercreator_mage',
        'charactercreator_necromancer',
        'charactercreator_thief',
    ]

    for table in rpg_table_list:
        temp_df = table_to_dataframe(table_name=table, connection=connection)
        # Insert data into mongodb
        db[table].insert_many(temp_df.to_dict(orient='records'))



    # Close Connection
    connection.close()
    client.close()