# Component Documentation

## 1. ChatApp (app.py)

### Purpose
Main application class that handles UI rendering and user interactions.

### Key Methods
```python
class ChatApp:
    def __init__(self):
        # Initializes the application and session state
        
    def initialize_session_state(self):
        # Sets up initial session variables
        
    def setup_ui(self):
        # Configures the main UI layout
        
    def setup_sidebar(self):
        # Configures the sidebar with database settings
        
    def handle_connection(self):
        # Manages database connections
        
    def process_user_query(self):
        # Processes user input and generates responses
```

### Session State Variables
- `chat_history`: List[BaseMessage]
- `is_connected`: bool
- `chat_manager`: ChatManager
- `db_config`: Dict[str, str]
- `current_viz`: Optional[Dict]

## 2. ChatManager (chat_manager.py)

### Purpose
Manages chat interactions, LLM operations, and coordinates between components.

### Key Methods
```python
class ChatManager:
    def __init__(self):
        # Initializes LLM and chains
        
    def _initialize_chains(self):
        # Sets up SQL and response chains
        
    def get_response(self):
        # Generates responses to user queries
        
    def _extract_visualization_params(self):
        # Extracts visualization parameters from responses
```

### LLM Integration
- Uses Groq's mistral-saba-24b model
- Implements two chain types:
  1. SQL Generation Chain
  2. Response Generation Chain

## 3. DatabaseManager (database.py)

### Purpose
Handles database connections, query execution, and result caching.

### Key Methods
```python
class DatabaseManager:
    def __init__(self, db_config):
        # Initializes database connection
        
    def _initialize_pool(self):
        # Sets up connection pool
        
    def execute_query(self):
        # Executes SQL queries
        
    def get_schema(self):
        # Retrieves and caches database schema
```

### Connection Pool Configuration
- Pool size: 5 connections
- Automatic cleanup
- Connection reuse
- Error handling

## 4. VisualizationManager (visualization_manager.py)

### Purpose
Creates and manages data visualizations.

### Key Methods
```python
class VisualizationManager:
    @staticmethod
    def create_visualization(data, viz_type, params):
        # Creates visualizations based on data and type
        
    @staticmethod
    def suggest_visualization(data):
        # Suggests appropriate visualization types
```

### Supported Chart Types
1. **Bar Charts**
   - Parameters: x, y, color, barmode
   - Use case: Categorical comparisons

2. **Line Charts**
   - Parameters: x, y, color
   - Use case: Time series, trends

3. **Scatter Plots**
   - Parameters: x, y, color, size
   - Use case: Correlations, distributions

4. **Pie Charts**
   - Parameters: values, names
   - Use case: Part-to-whole relationships

## 5. Configuration (config.py)

### Purpose
Manages application settings and configuration.

### Components
```python
class Settings(BaseSettings):
    # LLM Settings
    LLM_MODEL: str
    LLM_TEMPERATURE: float
    GROQ_API_KEY: str
    
    # Database Defaults
    DEFAULT_DB_HOST: str
    DEFAULT_DB_PORT: str
    # ... other settings
    
    # Visualization Settings
    SUPPORTED_CHARTS: ClassVar[List[str]]
    MAX_ROWS_DISPLAY: ClassVar[int]
```

### SQL Templates
1. **Default Template**
   - Purpose: SQL query generation
   - Components: schema, chat_history, question

2. **Response Template**
   - Purpose: Natural language response
   - Components: schema, query, response, visualization

## Error Handling

### 1. Database Errors
```python
try:
    # Database operations
except Exception as e:
    logger.error(f"Database error: {str(e)}")
    raise
```

### 2. LLM Errors
```python
try:
    # LLM operations
except Exception as e:
    logger.error(f"LLM error: {str(e)}")
    return error_message
```

### 3. Visualization Errors
```python
try:
    # Visualization creation
except Exception as e:
    logger.error(f"Visualization error: {str(e)}")
    return None
```

## Best Practices

### 1. Database Operations
- Always use connection pooling
- Close connections properly
- Use parameterized queries
- Implement proper error handling

### 2. LLM Operations
- Handle API errors gracefully
- Implement retry logic
- Validate responses
- Monitor token usage

### 3. UI Development
- Use containers for organization
- Implement proper state management
- Handle loading states
- Provide clear user feedback 