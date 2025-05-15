from typing import List, Optional, Dict, Any, Tuple
import logging
import re
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from config import settings, SQL_TEMPLATES
from database import DatabaseManager
from visualization_manager import VisualizationManager
import streamlit as st

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self):
        self.db_manager = DatabaseManager(st.session_state.db_config)
        self.viz_manager = VisualizationManager()
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.GROQ_API_KEY
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

    def _extract_visualization_params(self, response: str) -> Optional[Dict[str, Any]]:
        """Extract visualization parameters from the response."""
        viz_match = re.search(r'<VISUALIZATION\s+(.+?)>', response, re.DOTALL)
        if not viz_match:
            return None

        params = {}
        param_string = viz_match.group(1)
        
        # Extract type
        type_match = re.search(r'type="([^"]+)"', param_string)
        if type_match and type_match.group(1) in settings.SUPPORTED_CHARTS:
            params['type'] = type_match.group(1)
        else:
            return None

        # Extract other parameters
        for param in ['x', 'y', 'color', 'values', 'names', 'size']:
            param_match = re.search(f'{param}="([^"]+)"', param_string)
            if param_match:
                params[param] = param_match.group(1)

        return params

    def get_response(self, question: str, chat_history: List[BaseMessage]) -> Tuple[str, Optional[Dict]]:
        """Get response for user question with optional visualization."""
        try:
            # Get the response from the chain
            response = self.response_chain.invoke(
                {
                    "question": question,
                    "chat_history": chat_history,
                }
            )

            # Check for visualization request
            viz_params = self._extract_visualization_params(response)
            viz_data = None

            if viz_params:
                # Get the raw data from the last query
                raw_data = self.db_manager.get_last_query_data()
                
                # Create visualization
                viz_type = viz_params.pop('type')
                viz_data = self.viz_manager.create_visualization(
                    data=raw_data,
                    viz_type=viz_type,
                    params=viz_params
                )

                # Remove the visualization tag from the response
                response = re.sub(r'<VISUALIZATION\s+.+?>', '', response).strip()

            return response, viz_data

        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}", None

    def format_chat_history(self, messages: List[BaseMessage]) -> str:
        """Format chat history for prompt context."""
        formatted = []
        for msg in messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            formatted.append(f"{role}: {msg.content}")
        return "\n".join(formatted) 