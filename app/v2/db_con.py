from psycopg2 import connect
import os
def db_connection(db=None):
    """connects to the right db"""
    if 
    try:  
        con = connect(
                database=db,
                user=os.getenv('USER'),
                password=os.getenv('PASSWORD'),
                host=os.getenv('HOST'))
        return con
    except Exception as e:
        raise e
        
def user_table(curr):
    """Create User Table"""
    curr.execute(
        """
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL UNIQUE,
            password VARCHAR NOT NULL,
            role VARCHAR NOT NULL
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

def create(db=None):
    """create connection and all tables"""
    conn = db_connection(db=db)
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