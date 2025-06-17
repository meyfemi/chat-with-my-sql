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
                "host": "",
                "port": "",
                "user": "",
                "password": "",
                "database": ""
            }
        if "use_chat_history" not in st.session_state:
            st.session_state.use_chat_history = False

    def setup_ui(self):
        """Setup the Streamlit UI components."""
        st.title(settings.APP_TITLE)
        
        chat_col, viz_col = st.columns([2, 1])
        
        with st.sidebar:
            self.setup_sidebar()

        with chat_col:
            chat_container = st.container()
            
            # Display messages in the container
            with chat_container:
                for message in st.session_state.chat_history:
                    with st.chat_message("AI" if isinstance(message, AIMessage) else "Human"):
                        st.markdown(message.content)

            # Add the chat input at the bottom
            user_query = st.chat_input(
                "Ask a question or request a visualization...",
                disabled=not st.session_state.is_connected
            )
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
        st.write("Configure your MySQL database connection")
        
        with st.form("db_settings"):
            host = st.text_input("Host", value="localhost", placeholder="localhost")
            port = st.text_input("Port", value="3306", placeholder="3306")
            user = st.text_input("User", value="root", placeholder="root")
            password = st.text_input("Password", type="password", value="password", placeholder="password")
            database = st.text_input("Database", value="chinook", placeholder="chinook")
            
            if st.form_submit_button("Connect"):
                self.handle_connection(host, port, user, password, database)

        if st.session_state.is_connected:
            st.success("🟢 Connected to database")
            if st.button("Disconnect"):
                self.handle_disconnection()
        else:
            st.error("🔴 Not connected")
            
        # Add chat history toggle
        st.subheader("Chat Settings")
        use_history = st.toggle("Enable Chat History", value=st.session_state.use_chat_history)
        if use_history != st.session_state.use_chat_history:
            st.session_state.use_chat_history = use_history
            if not use_history:
                # Keep only the welcome message when disabling chat history
                st.session_state.chat_history = [st.session_state.chat_history[0]]
                st.rerun()

    def handle_connection(self, host: str, port: str, user: str, password: str, database: str):
        """Handle database connection attempt."""
        try:
            # Validate required fields
            if not all([host, port, user, database, password]):
                st.error("All fields are required. Please fill in all the connection details.")
                return
                
            # Validate port is numeric
            try:
                port = int(port)
            except ValueError:
                st.error("Port must be a valid number.")
                return

            with st.spinner("Connecting to database..."):
                # Store the database configuration
                db_config = {
                    "host": host,
                    "port": str(port),
                    "user": user,
                    "password": password,
                    "database": database
                }
                
                # Initialize database manager first
                db_manager = DatabaseManager(db_config)
                
                # Test connection by getting schema
                db_manager.get_schema()
                
                # Initialize chat manager with the database manager
                chat_manager = ChatManager(db_manager)
                
                # Store configurations and managers in session state
                st.session_state.db_config = db_config
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
            # Get chat history based on the toggle setting
            chat_history = st.session_state.chat_history if st.session_state.use_chat_history else [st.session_state.chat_history[0]]
            
            logger.info(f"Chat history: {chat_history}")

            # Show spinner while waiting for AI response
            with st.spinner("Thinking..."):
                response, viz_data = st.session_state.chat_manager.get_response(
                    question=user_query,
                    chat_history=chat_history
                )
            
            # Update visualization if available
            if viz_data:
                st.session_state.current_viz = viz_data
            
            # Add AI response to chat history
            st.session_state.chat_history.append(AIMessage(content=response))
            
            # If chat history is disabled, keep only the welcome message and the last exchange
            if not st.session_state.use_chat_history:
                st.session_state.chat_history = [
                    st.session_state.chat_history[0],  # Welcome message
                    st.session_state.chat_history[-2],  # User message
                    st.session_state.chat_history[-1]   # AI response
                ]
            
            # Rerun to update the UI
            st.rerun()
                    
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            st.rerun()

if __name__ == "__main__":
    app = ChatApp()
