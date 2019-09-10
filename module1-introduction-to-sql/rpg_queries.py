import sqlite3

'''
-
-
-
-
-
-
-
-
'''
# Helper Functions

## Establish a connection to database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('Connection to: ', db_file, ' successful')
    except Error as e:
        print(e)

    return conn

def query_total_char(conn):
    cursor =  conn.cursor()
    query = "SELECT character_id FROM charactercreator_character"
    cursor.execute(query)
    return len(cursor.fetchall())

def query_total_subclasses(conn, subclass_list):
    cursor = conn.cursor()
    subclass_totals = []
    for subclass in subclass_list:
        query = "SELECT * FROM charactercreator_" + subclass
        cursor.execute(query)
        subclass_totals.append((subclass, len(cursor.fetchall())))
    return subclass_totals

def query_total_items(conn):
    cursor = conn.cursor()
    query = "SELECT item_id FROM armory_item"
    cursor.execute(query)
    return len(cursor.fetchall())

def query_total_weapons(conn):
    cursor = conn.cursor()
    query = "SELECT item_ptr_id from armory_weapon"
    cursor.execute(query)
    return len(cursor.fetchall())

def query_char_items(conn, max_row):
    cursor_char = conn.cursor()
    cursor_inv = conn.cursor()
    query_char = "SELECT character_id FROM charactercreator_character LIMIT " + str(max_row)
    cursor_char.execute(query_char)
    characters = cursor_char.fetchall()
    character_inventories = []
    for character in characters:
        query_inv = "SELECT item_id from charactercreator_character_inventory WHERE character_id=?"
        cursor_inv.execute(query_inv, (character[0],))
        character_inventories.append({character[0]: cursor_inv.fetchall()})
    return character_inventories

def query_char_weapons(conn, max_row):
    cursor_char = conn.cursor()
    cursor_weapon = conn.cursor()
    query_char = "SELECT character_id FROM charactercreator_character LIMIT " + str(max_row)
    cursor_char.execute(query_char)
    characters = cursor_char.fetchall()
    character_weapons = []
    for character in characters:
        query_weapon = "SELECT item_id from charactercreator_character_inventory \
                            WHERE character_id=? \
                            AND item_id IN \
                                (SELECT item_ptr_id from armory_weapon)"
        cursor_weapon.execute(query_weapon, (character[0],))
        character_weapons.append({
            character[0]: cursor_weapon.fetchall()
        })
    return character_weapons

db_file_name = 'rpg_db.sqlite3'
character_subclasses = ['cleric', 'fighter', 'mage', 'necromancer', 'thief']
connection = create_connection(db_file_name)

'''
    PART 1: Querying DB
    Use `sqlite3` to load and write queries to explore the data
'''

with connection as conn:
    # How many total Characters are there?
    total_char = query_total_char(conn)
    print(total_char, 'Total Characters')
    # How many of each specific subclass?
    total_subclasses = query_total_subclasses(conn, character_subclasses)
    print(total_subclasses)
    # How many total Items?
    total_items = query_total_items(conn)
    print(total_items, 'Total Items')
    # How many of the Items are weapons? How many are not?
    total_weapons = query_total_weapons(conn)
    print(total_weapons, 'Total Weapons.  ',
            total_items - total_weapons, ' items are not weapons')
    # How many Items does each character have? (Return first 20 rows)
    char_items = query_char_items(conn, 20)
    print("First 20 Character's Items")
    print(char_items)
    # How many Weapons does each character have? (Return first 20 rows)
    print("First 20 Character's Weapons")
    char_weapons = query_char_weapons(conn, 20)
    print(char_weapons)
    # On average, how many Items does each Character have?
    char_items = query_char_items(conn, 500)
    items_sum = 0
    for char_set in char_items:
        # print(list(char_set.values())[0]) # debug
        items_sum += len(list(char_set.values())[0])
    print('average items:', items_sum/len(char_items))
    # On average, how many Weapons does each character have?
    char_weapons = query_char_weapons(conn, 500)
    weapons_sum = 0
    for char_set in char_weapons:
        # print(char_set.values()) # debug
        weapons_sum += len(list(char_set.values())[0])
    print('average weapons:', weapons_sum/len(char_weapons))