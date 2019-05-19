from psycopg2 import connect
import os
def db_connection(db_name):
    """connects to db"""
    try:  
        con = connect(
                database=db_name,
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'))
        return con
    except Exception as e:
        raise e

# db_url = os.getenv('DATABASE_URI')
# conn = db_connection("ireporter")



# con = psycopg2.connect(db_url)

def user_table(curr):
    """Create User Table"""
    curr.execute(
        """
        CREATE TABLE users(
            id serial PRIMARY KEY,
            role VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL UNIQUE,
            password VARCHAR NOT NULL
        );
        """
    )

def incidents_table(curr):
    """Create incidents table"""
    curr.execute(
        """
        CREATE TABLE incidents(
            id serial PRIMARY KEY,
            comment VARCHAR NOT NULL,
            location VARCHAR NOT NULL,
            created_by INTEGER NOT NULL,
            FOREIGN KEY(created_by) REFERENCES users(id) ON DELETE CASCADE
        );
        """
    )

def create():
    """create connection and all tables"""
    conn = db_connection("ireporter")
    if not isinstance(conn, str):
        print('success')
    else:
        print (conn)
        print('Failed to connect')
    conn.set_session(autocommit=True)
    curr = conn.cursor()
    curr.execute(
        """DROP TABLE IF EXISTS users, incidents CASCADE
        """
    )
    user_table(curr)
    incidents_table(curr)

    curr.close()
    conn.commit()

if __name__=="__main__":
    create()