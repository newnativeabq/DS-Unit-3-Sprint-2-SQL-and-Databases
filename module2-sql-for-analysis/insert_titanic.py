import psycopg2

import setup
import os

setup.commit_environ_vars()

# Database Connection
def make_remote_connection():
    pg_conn = psycopg2.connect(
        dbname = os.environ.get('dbname'),
        user = os.environ.get('user'),
        password = os.environ.get('password'),
        host = os.environ.get('host'),
    )
    return pg_conn

# Schema Development
titanic_columns = {
    "Survived": ['bit'],
    "Pclass": ,
    "Name": ,
    "Sex": ,
    "Age": ,
    "Siblings/Spouses Aboard": ,
    "Parents/Children Aboard": ,
    "Fare": ,
}

if __name__ == "__main__":
    connection = make_connection()
    print(type(connection))