import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Database:
    _connection = None  # Singleton instance

    @classmethod
    def get_connection(cls):
        """Return an existing connection or create a new one if not available."""
        if cls._connection is None or not cls._connection.is_connected():
            cls._connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=int(os.getenv("DB_PORT", 3306))
            )
        return cls._connection

    @classmethod
    def close_connection(cls):
        """Close the database connection."""
        if cls._connection and cls._connection.is_connected():
            cls._connection.close()
            cls._connection = None

# Dependency to get the database connection
def get_db():
    """Dependency for FastAPI routes to get a database connection."""
    db = Database.get_connection()
    try:
        yield db
    finally:
        Database.close_connection()
