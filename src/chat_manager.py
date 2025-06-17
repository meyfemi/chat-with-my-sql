from typing import List, Optional, Dict, Any
import logging
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from config import settings, SQL_TEMPLATES
from database import DatabaseManager

logger = logging.getLogger(__name__)


class ChatManager:
    def __init__(self, db_manager: DatabaseManager):
        """Initialize ChatManager with a DatabaseManager instance."""
        self.db_manager = db_manager
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        self._initialize_chains()

    def _initialize_chains(self):
        """Initialize the SQL and response chains."""
        # SQL Chain
        sql_prompt = ChatPromptTemplate.from_template(SQL_TEMPLATES["default"])
        self.sql_chain = (
                RunnablePassthrough.assign(schema=lambda _: self.db_manager.get_schema())
                | sql_prompt
                | self.llm
                | StrOutputParser()
        )

        # Response Chain
        response_prompt = ChatPromptTemplate.from_template(SQL_TEMPLATES["response"])
        self.response_chain = (
                RunnablePassthrough.assign(query=self.sql_chain).assign(
                    schema=lambda _: self.db_manager.get_schema(),
                    response=lambda vars: self.db_manager.execute_query(vars['query']),
                )
                | response_prompt
                | self.llm
                | StrOutputParser()
        )

    def get_response(self, question: str, chat_history: List[BaseMessage]) -> tuple[str, Optional[Dict[str, Any]], str]:
        """Get response for user question and any visualization data.
        
        Returns:
            tuple: (response_text, visualization_data, sql_query)
        """
        try:
            # Format chat history if it contains more than just the welcome message
            formatted_history = self.format_chat_history(chat_history) if len(chat_history) > 1 else ""

            # Get the SQL query first
            sql_query = self.sql_chain.invoke(
                {
                    "question": question,
                    "chat_history": formatted_history,
                }
            )

            # Get the response using the generated SQL
            response = self.response_chain.invoke(
                {
                    "question": question,
                    "chat_history": formatted_history,
                    "query": sql_query
                }
            )

            # Extract visualization data if present
            viz_data = None
            if "<VISUALIZATION" in response:
                try:
                    # Extract visualization parameters
                    viz_start = response.find("<VISUALIZATION")
                    viz_end = response.find(">", viz_start) + 1
                    viz_tag = response[viz_start:viz_end]

                    # Remove the visualization tag from the response
                    response = response.replace(viz_tag, "").strip()
                    # Parse visualization parameters
                    import re
                    params = dict(re.findall(r'(\w+)="([^"]*)"', viz_tag))

                    viz_type = params.pop("type", "bar")  # Default to bar chart

                    # Get the last query data from database manager
                    data = self.db_manager.get_last_query_data()
                    if data is not None:
                        from visualization_manager import VisualizationManager
                        viz_data = VisualizationManager.create_visualization(data, viz_type, params)
                except Exception as e:
                    logger.error(f"Error creating visualization: {str(e)}")
                    # Continue without visualization if there's an error

            return response, viz_data, sql_query

        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}", None, ""

    def format_chat_history(self, messages: List[BaseMessage]) -> str:
        """Format chat history for prompt context."""
        # Skip the welcome message (first message) when formatting history
        formatted = []
        for msg in messages[1:]:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            formatted.append(f"{role}: {msg.content}")
        return "\n".join(formatted)
