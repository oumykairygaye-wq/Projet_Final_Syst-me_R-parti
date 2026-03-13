import sqlite3
from queue import Queue

# Taille du pool de connexions
POOL_SIZE = 5

# Création du pool
connection_pool = Queue(maxsize=POOL_SIZE)


def init_database():
    

    conn = sqlite3.connect("monitoring.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_name TEXT,
        last_seen TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_name TEXT,
        cpu REAL,
        memory REAL,
        uptime INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_connection_pool():
    

    for _ in range(POOL_SIZE):
        conn = sqlite3.connect("monitoring.db", check_same_thread=False)
        connection_pool.put(conn)


def get_connection():
    
    return connection_pool.get()


def release_connection(conn):
   
    connection_pool.put(conn)