from typing import Dict, Any, ClassVar, List
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # LLM settings (from environment variables)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Cache settings
    SCHEMA_CACHE_TTL: int = 3600  # 1 hour
    
    # App settings
    APP_TITLE: str = "Chat with MySQL"
    APP_ICON: str = ":robot_face:"
    
    # Visualization settings
    SUPPORTED_CHARTS: ClassVar[List[str]] = ["bar", "line", "scatter", "pie"]
    MAX_ROWS_DISPLAY: ClassVar[int] = 1000
    
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
    
    IMPORTANT: For MySQL, window functions (like AVG(...) OVER (...)) are only allowed in the SELECT and ORDER BY clauses. If you need to filter based on a window function, use a subquery or CTE to first compute the window function, then filter in the outer query. Do NOT use window functions directly in the WHERE clause.
    
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
    
    Write a direct, concise response without any introductory phrases like "Based on the SQL query and response". Just state the facts and suggest a visualization if appropriate.
    
    If the data is suitable for visualization, end your response with one of these tags:
    <VISUALIZATION type="bar|line|scatter|pie" x="column_name" y="column_name" [color="column_name"] [values="column_name"] [names="column_name"]>
    
    For example:
    Question: How many customers are from the UAE?
    Response: There are 140 customers from the UAE. This data could be visualized using a pie chart to show the distribution of customers by country.
    <VISUALIZATION type="pie" values="count" names="country">
    """
}