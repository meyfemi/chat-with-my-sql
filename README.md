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