from typing import Dict, Any, ClassVar, List
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # LLM settings (from environment variables)
    LLM_MODEL: str = "mistral-saba-24b"
    LLM_TEMPERATURE: float = 0.0
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Cache settings
    SCHEMA_CACHE_TTL: int = 3600  # 1 hour
    
    # App settings
    APP_TITLE: str = "Chat with MySQL"
    APP_ICON: str = ":robot_face:"
    
    # Visualization settings
    SUPPORTED_CHARTS: ClassVar[List[str]] = ["bar", "line", "scatter", "pie"]
    MAX_ROWS_DISPLAY: ClassVar[int] = 1000
    
    # Default database settings (can be overridden by UI)
    DEFAULT_DB_HOST: str = "localhost"
    DEFAULT_DB_PORT: str = "3306"
    DEFAULT_DB_USER: str = "root"
    DEFAULT_DB_PASSWORD: str = "password"
    DEFAULT_DB_NAME: str = "sql_training"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

# SQL Templates
SQL_TEMPLATES: Dict[str, str] = {
    "default": """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    If the user asks for visualization or charts, make sure to include relevant numerical and categorical columns in the query.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: Name 10 customers first names
    SQL Query: SELECT first_name FROM customers LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """,
    
    "response": """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    If the query result contains numerical data that could be visualized, suggest a visualization type (bar, line, scatter, or pie chart).
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}
    
    If the data is suitable for visualization, end your response with one of these tags:
    <VISUALIZATION type="bar|line|scatter|pie" x="column_name" y="column_name" [color="column_name"] [values="column_name"] [names="column_name"]>
    
    For example:
    This data shows sales by category. I've created a bar chart to better visualize this distribution.
    <VISUALIZATION type="bar" x="category" y="sales" color="region">
    """
} 