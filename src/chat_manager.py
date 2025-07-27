from typing import List, Optional, Dict, Any
import logging
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import settings, SQL_TEMPLATES
from database import DatabaseManager
import google.generativeai as genai

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self, db_manager: DatabaseManager):
        """Initialize ChatManager with a DatabaseManager instance."""
        self.db_manager = db_manager
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def get_gemini_completion(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    def get_response(self, question: str, chat_history: List[BaseMessage]) -> tuple[str, Optional[Dict[str, Any]], str]:
        """Get response for user question and any visualization data.
        
        Returns:
            tuple: (response_text, visualization_data, sql_query)
        """
        try:
            formatted_history = self.format_chat_history(chat_history) if len(chat_history) > 1 else ""

            # Compose SQL prompt
            sql_prompt = SQL_TEMPLATES["default"].format(
                schema=self.db_manager.get_schema(),
                chat_history=formatted_history,
                question=question
            )
            sql_query = self.get_gemini_completion(sql_prompt).strip()

            # Compose response prompt
            sql_response = self.db_manager.execute_query(sql_query)
            response_prompt = SQL_TEMPLATES["response"].format(
                schema=self.db_manager.get_schema(),
                chat_history=formatted_history,
                query=sql_query,
                question=question,
                response=sql_response
            )
            response = self.get_gemini_completion(response_prompt).strip()

            # Extract visualization data if present
            viz_data = None
            if "<VISUALIZATION" in response:
                try:
                    viz_start = response.find("<VISUALIZATION")
                    viz_end = response.find(">", viz_start) + 1
                    viz_tag = response[viz_start:viz_end]
                    response = response.replace(viz_tag, "").strip()
                    import re
                    params = dict(re.findall(r'(\w+)="([^"]*)"', viz_tag))
                    viz_type = params.pop("type", "bar")
                    data = self.db_manager.get_last_query_data()
                    if data is not None:
                        from visualization_manager import VisualizationManager
                        viz_data = VisualizationManager.create_visualization(data, viz_type, params)
                except Exception as e:
                    logger.error(f"Error creating visualization: {str(e)}")
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
