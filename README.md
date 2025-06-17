# Chat with MySQL

A production-ready Streamlit application that allows users to interact with MySQL databases using natural language queries. The application uses LangChain and Groq's LLM to convert natural language questions into SQL queries and provide human-readable responses.

## Features

- Natural language to SQL query conversion
- Interactive chat interface
- Connection pooling for efficient database access
- Error handling and logging
- Configurable settings via environment variables
- Clean and modern UI
- Session management
- Caching for improved performance

## Prerequisites

- Python 3.8+
- MySQL Server
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chat-with-mysql
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your configuration:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
GROQ_API_KEY=your_groq_api_key
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Configure your database connection using the sidebar settings

4. Start chatting with your database!

## Project Structure

```
chat-with-mysql/
├── src/
│   ├── app.py           # Main Streamlit application
│   ├── chat_manager.py  # Chat and LLM interaction logic
│   ├── config.py        # Configuration management
│   └── database.py      # Database connection and query handling
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## How Data Flows

User Types Question → ChatApp → ChatManager → LLM → SQL Query → Database → Results → Visualization → Display 

## Key Classes and Their Roles

### ChatApp

```python
class ChatApp:
    def __init__(self)  # Initializes the app
    def setup_ui()      # Creates the interface
    def setup_sidebar() # Handles database settings
    def process_user_query() # Processes user messages
```

### ChatManager

```python
class ChatManager:
    def __init__(db_manager)     # Sets up AI and database connection
    def get_response()           # Gets AI response
    def format_chat_history()    # Formats conversation history
```

### DatabaseManager

```python
class DatabaseManager:
    def __init__(db_config)      # Sets up database connection
    def execute_query()          # Runs SQL queries
    def get_schema()            # Gets database structure
```

### VisualizationManager

```python
class VisualizationManager:
    def __init__(self)  # Initializes the manager
    def create_chart()  # Creates a chart based on query results
    def display_chart() # Displays the created chart
```

## Key Features

### Database Connection

- Connect via sidebar
- Enter host, port, user, password, database
- Connection status shown
- Secure credential handling

### Chat Interface

- Natural language queries
- Chat history (can be toggled on/off)
- Error handling
- Real-time responses

### Visualizations

- Automatic chart creation
- Multiple chart types (bar, line, scatter, pie)
- Interactive Plotly charts
- Data limit handling

## How to Use

```bash
# 1. Start the app
streamlit run src/app.py

# 2. Connect to database:
- Fill in database details in sidebar
- Click "Connect"

# 3. Start chatting:
- Type natural language questions
- Get SQL results and visualizations
- Toggle chat history if needed
```

## Important Settings

- Chat history toggle in sidebar
- Database connection settings
- Visualization options
- Error messages and logging

## Error Handling

- Database connection errors
- Query execution errors
- Visualization errors
- Input validation

Would you like me to explain any specific part in more detail? For example:
1. The database connection flow
2. How natural language is converted to SQL
3. How visualizations are created
4. The chat history management
5. Error handling in different components 