# PDF Chat Bot

A Streamlit-based application that allows users to upload PDF documents and interact with them using natural language queries. The application uses LlamaIndex for document processing and Groq's LLM for generating responses.

## Features

- PDF document upload and processing
- Natural language querying of PDF content
- Interactive chat interface
- Chat history tracking
- Real-time response generation

## Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd self-pdf-bot
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -e .
```

## Configuration

The application uses the following services:
- Groq LLM API for text generation
- Qdrant for vector storage

Make sure you have the necessary API keys and credentials set up.

## Running the Application

### Running UI App
1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

### Running Console App
1. Start the application:
```bash
uv run app.py
```

## Usage

1. Upload a PDF document using the file uploader
2. Wait for the document to be processed (you'll see a success message)
3. Start asking questions about the content of your PDF in the chat interface
4. View the chat history and responses in real-time

## Project Structure

- `app.py`: Main Streamlit application file
- `main.py`: Core PDF processing and querying logic
- `pyproject.toml`: Project dependencies and metadata

## Dependencies

- streamlit: Web application framework
- llama-index: Document processing and querying
- groq: LLM integration
- qdrant-client: Vector database client
