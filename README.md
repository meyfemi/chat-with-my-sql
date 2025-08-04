# Chat with MySQL

A production-ready Streamlit application that allows users to interact with MySQL databases using natural language queries. The application uses Google Gemini AI to convert natural language questions into SQL queries and provide human-readable responses with automatic visualizations.

## Features

- Natural language to SQL query conversion
- Interactive chat interface with real-time responses
- Automatic data visualization using Plotly
- Connection pooling for efficient database access
- Error handling and logging
- Configurable settings via environment variables
- Clean and modern UI
- Session management
- Caching for improved performance
- Docker support for easy deployment

## Prerequisites

- Docker and Docker Compose
- MySQL database (local or remote)
- Google Gemini API key

## Quick Start with Docker (Recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd chat-with-mysql
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
```

### 3. Run with Docker Compose
```bash
# Build and start the application
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application
- Open your web browser
- Navigate to: **http://localhost:8501**
- Configure your database connection in the sidebar
- Start chatting with your database!

## Database Connection Setup

### For Local MySQL Database:
1. **Enable remote connections** in MySQL:
   ```bash
   # Edit MySQL config file (location may vary)
   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
   ```

2. **Change bind-address** in the `[mysqld]` section:
   ```ini
   [mysqld]
   bind-address = 0.0.0.0  # Allow connections from any IP
   ```

3. **Restart MySQL service:**
   ```bash
   sudo systemctl restart mysql
   ```

4. **Grant permissions** for your user:
   ```sql
   -- Connect to MySQL as root
   mysql -u root -p
   
   -- Grant permissions (replace with your actual username and database)
   GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'%' IDENTIFIED BY 'your_password';
   FLUSH PRIVILEGES;
   ```

5. **Connection settings in the app:**
   - Host: `host.docker.internal` (Docker's hostname for your computer)
   - Port: `3306`
   - User: Your MySQL username
   - Password: Your MySQL password
   - Database: Your database name

### For Remote MySQL Database:
- Ensure your MySQL server allows external connections
- Configure firewall rules to allow connections on port 3306
- Use the remote server's IP address or hostname in the connection settings

## Docker Commands

```bash
# Start the application
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild and start (if you make code changes)
docker-compose up --build

# Stop and remove containers, networks, and volumes
docker-compose down -v
```

## Local Development Setup (Alternative)

If you prefer to run the application locally without Docker:

### Prerequisites
- Python 3.8+
- MySQL Server
- Google Gemini API key

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd chat-with-mysql
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run src/app.py
   ```

## Usage

### Connecting to Your Database
1. **Open the application** in your web browser
2. **Configure database connection** in the sidebar:
   - Host: Your MySQL server hostname/IP
   - Port: Your MySQL port (usually 3306)
   - User: Your MySQL username
   - Password: Your MySQL password
   - Database: Your database name
3. **Click "Connect"** to establish the connection

### Chatting with Your Database
1. **Ask questions** in natural language:
   - "Show me the top 10 customers by total purchases"
   - "Which products had the highest sales last month?"
   - "Find customers who haven't made a purchase in 6 months"

2. **View results** including:
   - Natural language responses
   - Generated SQL queries (for transparency)
   - Automatic visualizations (when applicable)

3. **Toggle features** in the sidebar:
   - Chat history (on/off)
   - Database connection settings

## Project Structure

```
chat-with-mysql/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── chat_manager.py     # Chat and AI interaction logic
│   ├── config.py           # Configuration management
│   ├── database.py         # Database connection and query handling
│   └── visualization_manager.py  # Data visualization logic
├── .env                    # Environment variables (create this)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .dockerignore          # Docker ignore file
└── README.md              # This file
```

## Troubleshooting

### Docker Issues
- **Container won't start**: Check if port 8501 is available
- **Build fails**: Ensure Docker and Docker Compose are installed
- **Permission errors**: Run with appropriate user permissions

### Database Connection Issues
- **Connection refused**: Check if MySQL is running and accessible
- **Access denied**: Verify user permissions and host access
- **Firewall issues**: Ensure port 3306 is open

### API Issues
- **429 errors**: Check your Gemini API quota and rate limits
- **Authentication errors**: Verify your API key in the `.env` file

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