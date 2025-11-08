import psycopg2
from psycopg2 import pool
from config.settings import DB_CONFIG
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    _connection_pool = None
    
    @classmethod
    def initialize_pool(cls, minconn=1, maxconn=10):
        """Initialize the connection pool"""
        try:
            cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn, maxconn, **DB_CONFIG
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Error initializing connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._connection_pool is None:
            cls.initialize_pool()
        return cls._connection_pool.getconn()
    
    @classmethod
    def return_connection(cls, conn):
        """Return a connection to the pool"""
        if cls._connection_pool:
            cls._connection_pool.putconn(conn)
    
    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._connection_pool:
            cls._connection_pool.closeall()
            logger.info("All database connections closed")

def get_db_connection():
    """Helper function to get a database connection"""
    return DatabaseManager.get_connection()

def execute_query(query, params=None, fetch=False):
    """Execute a query and optionally fetch results"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch:
            results = cursor.fetchall()
            conn.commit()
            return results
        else:
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error executing query: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            DatabaseManager.return_connection(conn)