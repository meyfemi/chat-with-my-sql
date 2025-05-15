# Chat with MySQL Documentation

## Overview
Chat with MySQL is an interactive application that allows users to query MySQL databases using natural language. It combines the power of LangChain, Groq's LLM, and Streamlit to provide a chat interface where users can:
- Query databases using plain English
- Visualize query results with interactive charts
- Explore data through natural conversations

## Key Features
- Natural language to SQL conversion
- Interactive chat interface
- Real-time data visualization
- Database connection management
- Error handling and logging
- Session management
- Responsive UI with fixed chat input

## Tech Stack
- **Frontend**: Streamlit
- **Language Model**: Groq (mistral-saba-24b)
- **Database**: MySQL
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **ORM**: SQLAlchemy
- **Other Tools**: LangChain, python-dotenv

## Project Structure
```
chat-with-mysql/
├── src/
│   ├── app.py           # Main application and UI logic
│   ├── chat_manager.py  # Chat and LLM interaction handling
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection and query handling
│   └── visualization_manager.py  # Data visualization logic
├── docs/               # Documentation
├── .env               # Environment variables (create this)
├── requirements.txt   # Python dependencies
└── README.md         # Project overview
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL Server
- Groq API key

### Installation
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

4. Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
```

### Running the Application
```bash
streamlit run src/app.py
```

## Configuration
The application can be configured through:
1. Environment variables in `.env`
2. UI settings in the sidebar
3. Constants in `config.py`

### Default Settings
- Database connection defaults (configurable via UI)
- LLM model and temperature
- Visualization settings
- Cache settings

## Usage Guide
1. Start the application
2. Configure database connection in the sidebar
3. Connect to your database
4. Start chatting and querying your data
5. Request visualizations when needed

## Security Considerations
- Database credentials are stored in session state
- Passwords are masked in the UI
- API keys are loaded from environment variables
- Connection pooling with limited connections

## For more detailed documentation:
- [Architecture Guide](./architecture.md)
- [Component Documentation](./components.md)
- [API Documentation](./api.md)
- [Development Guide](./development.md) 