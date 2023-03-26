import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def execute_query(conn, exec_sql):
    """
    Execute a query from the exec_sql statement
    @param conn Connection object
    @param exec_sql an exec statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(exec_sql)
    except Error as e:
        print(e)

def main():
    database = './data/currency.db'

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        # Create Users table
        execute_query(conn, '''
            CREATE TABLE IF NOT EXISTS Users(
                Id INTEGER PRIMARY KEY,
                DiscordId INTEGER NOT NULL,
                ServerId INTEGER NOT NULL
            );
        ''')

        # Create Balances table
        execute_query(conn, '''
            CREATE TABLE IF NOT EXISTS Balance(
                Id INTEGER PRIMARY KEY,
                Balance REAL NOT NULL
            );
        ''')
        
        # Create TransactionLog table
        execute_query(conn, '''
            CREATE TABLE IF NOT EXISTS TransactionLog(
                Id INTEGER PRIMARY KEY,
                Description TEXT,
                Change REAL NOT NULL
            );
        ''')

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()