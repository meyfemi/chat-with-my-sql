from typing import Optional, Any, Dict
from functools import lru_cache
import logging
import pandas as pd
from mysql.connector.pooling import MySQLConnectionPool
from langchain_community.utilities import SQLDatabase
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None
    _pool: Optional[MySQLConnectionPool] = None
    _db: Optional[SQLDatabase] = None
    _last_query_data: Any = None
    _db_config: Dict[str, str] = None

    def __new__(cls, db_config: Dict[str, str] = None):
        if cls._instance is None or db_config != cls._db_config:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._db_config = db_config
            cls._pool = None
            cls._db = None
        return cls._instance

    def __init__(self, db_config: Dict[str, str] = None):
        if not self._pool or db_config != self._db_config:
            self._db_config = db_config
            self._initialize_pool()

    def _initialize_pool(self):
        try:
            dbconfig = {
                "host": self._db_config["host"],
                "port": self._db_config["port"],
                "user": self._db_config["user"],
                "password": self._db_config["password"],
                "database": self._db_config["database"],
                "pool_name": "mypool",
                "pool_size": 5,
            }
            self._pool = MySQLConnectionPool(**dbconfig)
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {str(e)}")
            raise

    @property
    def db(self) -> SQLDatabase:
        if not self._db:
            try:
                dburl = f"mysql+mysqlconnector://{self._db_config['user']}:{self._db_config['password']}@{self._db_config['host']}:{self._db_config['port']}/{self._db_config['database']}"
                self._db = SQLDatabase.from_uri(dburl)
            except Exception as e:
                logger.error(f"Failed to create SQLDatabase instance: {str(e)}")
                raise
        return self._db

    @lru_cache(maxsize=1)
    def get_schema(self) -> str:
        """Get database schema with caching."""
        try:
            return self.db.get_table_info()
        except Exception as e:
            logger.error(f"Failed to get database schema: {str(e)}")
            raise

    def execute_query(self, query: str) -> str:
        """Execute a SQL query with error handling."""
        try:
            # Execute query using SQLAlchemy for better DataFrame support
            with self.db._engine.connect() as connection:
                result = pd.read_sql_query(query, connection)
                
                # Store the result for visualization
                if len(result) > settings.MAX_ROWS_DISPLAY:
                    self._last_query_data = result.head(settings.MAX_ROWS_DISPLAY)
                    logger.warning(f"Query returned {len(result)} rows, truncating to {settings.MAX_ROWS_DISPLAY}")
                else:
                    self._last_query_data = result
                
                # Convert to string representation for chat response
                return result.to_string()
        except Exception as e:
            logger.error(f"Failed to execute query: {str(e)}")
            raise

    def get_last_query_data(self) -> Optional[pd.DataFrame]:
        """Get the data from the last executed query."""
        return self._last_query_data

    def close(self):
        """Close all database connections."""
        try:
            if self._db:
                # Close SQLAlchemy engine connections
                self._db._engine.dispose()
                self._db = None
            
            # Clear the connection pool
            self._pool = None
            
            # Clear cached data
            self._last_query_data = None
            self.get_schema.cache_clear()
            
            logger.info("Database connections closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connections: {str(e)}")
            raise