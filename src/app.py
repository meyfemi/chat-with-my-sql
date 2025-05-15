import logging
import streamlit as st
from typing import Optional, Dict, Any
from config import settings
from database import DatabaseManager
from chat_manager import ChatManager
from langchain_core.messages import AIMessage, HumanMessage

# Must be the first Streamlit command
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon=settings.APP_ICON,
    layout="wide"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add custom CSS to fix chat input at bottom
st.markdown("""
<style>
.stChatFloatingInputContainer {
    position: fixed !important;
    bottom: 0 !important;
    background: #0E1117 !important;
    padding: 1rem !important;
    z-index: 1000 !important;
    width: 48% !important;
}

.main {
    padding-bottom: 80px !important;
}

[data-testid="column"] [data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

class ChatApp:
    def __init__(self):
        self.initialize_session_state()
        self.setup_ui()
        
    def initialize_session_state(self):
        """Initialize session state variables."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello! I'm ready to help you query your MySQL database. "
                         "You can ask questions and request visualizations of the data. "
                         "Please connect to your database using the sidebar settings.")
            ]
        if "is_connected" not in st.session_state:
            st.session_state.is_connected = False
        if "chat_manager" not in st.session_state:
            st.session_state.chat_manager = None
        if "db_config" not in st.session_state:
            st.session_state.db_config = {
                "host": settings.DEFAULT_DB_HOST,
                "port": settings.DEFAULT_DB_PORT,
                "user": settings.DEFAULT_DB_USER,
                "password": settings.DEFAULT_DB_PASSWORD,
                "database": settings.DEFAULT_DB_NAME
            }

    def setup_ui(self):
        """Setup the Streamlit UI components."""
        st.title(settings.APP_TITLE)
        
        # Create two columns for chat and visualization
        chat_col, viz_col = st.columns([2, 1])
        
        # Sidebar configuration
        with st.sidebar:
            self.setup_sidebar()

        # Main chat interface
        with chat_col:
            # Create a container for messages with bottom padding
            chat_container = st.container()
            
            # Add the chat input at the bottom
            user_query = st.chat_input(
                "Ask a question or request a visualization...",
                disabled=not st.session_state.is_connected
            )
            
            # Display messages in the container
            with chat_container:
                for message in st.session_state.chat_history:
                    with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
                        st.markdown(message.content)
            
            # Process user input if provided
            if user_query:
                self.process_user_query(user_query)
            
        # Visualization area
        with viz_col:
            if "current_viz" in st.session_state and st.session_state.current_viz:
                st.subheader("Data Visualization")
                viz_data = st.session_state.current_viz
                if viz_data and "figure" in viz_data:
                    st.plotly_chart(viz_data["figure"], use_container_width=True)

    def setup_sidebar(self):
        """Setup the sidebar with database connection settings."""
        st.subheader("Database Settings")
        st.write("Configure your MySQL database connection:")
        
        with st.form("db_settings"):
            host = st.text_input("Host", settings.DEFAULT_DB_HOST)
            port = st.text_input("Port", settings.DEFAULT_DB_PORT)
            user = st.text_input("User", settings.DEFAULT_DB_USER)
            password = st.text_input("Password", type="password", value=settings.DEFAULT_DB_PASSWORD)
            database = st.text_input("Database", settings.DEFAULT_DB_NAME)
            
            if st.form_submit_button("Connect"):
                self.handle_connection(host, port, user, password, database)

        if st.session_state.is_connected:
            st.success("🟢 Connected to database")
            if st.button("Disconnect"):
                self.handle_disconnection()
        else:
            st.error("🔴 Not connected")

    def handle_connection(self, host: str, port: str, user: str, password: str, database: str):
        """Handle database connection attempt."""
        try:
            with st.spinner("Connecting to database..."):
                # Store the database configuration
                st.session_state.db_config = {
                    "host": host,
                    "port": port,
                    "user": user,
                    "password": password,
                    "database": database
                }
                
                # Initialize managers with the current configuration
                db_manager = DatabaseManager(st.session_state.db_config)
                chat_manager = ChatManager()
                
                # Test connection by getting schema
                db_manager.get_schema()
                
                # Store chat manager in session state
                st.session_state.chat_manager = chat_manager
                st.session_state.is_connected = True
                
                st.success("Successfully connected to database!")
                
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            st.error(f"Failed to connect to database: {str(e)}")
            st.session_state.is_connected = False

    def handle_disconnection(self):
        """Handle database disconnection."""
        try:
            if st.session_state.chat_manager:
                st.session_state.chat_manager.db_manager.close()
            st.session_state.is_connected = False
            st.session_state.chat_manager = None
            st.session_state.current_viz = None
            st.success("Disconnected from database")
        except Exception as e:
            logger.error(f"Error during disconnection: {str(e)}")
            st.error(f"Error during disconnection: {str(e)}")

    def process_user_query(self, user_query: str):
        """Process user query and generate response."""
        if not user_query.strip():
            return

        # Add user message to chat
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        try:
            response, viz_data = st.session_state.chat_manager.get_response(
                question=user_query,
                chat_history=st.session_state.chat_history
            )
            
            # Update visualization if available
            if viz_data:
                st.session_state.current_viz = viz_data
            
            # Add AI response to chat history
            st.session_state.chat_history.append(AIMessage(content=response))
            
            # Rerun to update the UI
            st.rerun()
                    
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)

if __name__ == "__main__":
    app = ChatApp()
