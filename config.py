"""Configuration settings for the application"""

# Qdrant settings
QDRANT_HOST = "localhost"  # Change this to your Qdrant host
QDRANT_PORT = 6333
QDRANT_API_KEY = ""  # Add your API key here

# LLM settings
LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# Application settings
APP_PORT = 8501  # Streamlit default port 