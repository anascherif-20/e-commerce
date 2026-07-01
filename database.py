import mysql.connector
from mysql.connector import pooling

connection_pool = pooling.MySQLConnectionPool(
    pool_name="ecommerce_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="",
    database="ecommerce"
)


def get_db():
    """Return a fresh (connection, cursor) pair from the pool."""
    conn = connection_pool.get_connection()
    cur = conn.cursor(dictionary=True)
    return conn, cur
