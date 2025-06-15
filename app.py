"""STREAMLIT APP"""
import streamlit as st
import tempfile
import os
import logging
import sys
from pathlib import Path

import qdrant_client
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from llama_index.llms.groq import Groq

from config import *  # Import all configuration variables

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Initialize settings
Settings.embed_model = FastEmbedEmbedding(model_name=EMBEDDING_MODEL)
Settings.llm = Groq(model=LLM_MODEL)

# Initialize Qdrant client
client = qdrant_client.QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    api_key=QDRANT_API_KEY
)

def collection_exists(collection_name: str) -> bool:
    try:
        client.get_collection(collection_name=collection_name)
        return True
    except Exception as e:
        return False

def process_pdf(pdf_file):
    """Process uploaded PDF and create index"""
    # Create a temporary directory to store the PDF
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded file
        temp_file_path = os.path.join(temp_dir, pdf_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        # Load and process the document
        documents = SimpleDirectoryReader(temp_dir).load_data()
        
        # Create vector store and index
        vector_store = QdrantVectorStore(client=client, collection_name=str(pdf_file.name))
        
        if collection_exists(str(pdf_file.name)):
            index = VectorStoreIndex.from_vector_store(vector_store)
            logging.info(f"Loaded index for {pdf_file.name}")
            return index.as_query_engine()
        else:
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex.from_documents(
                documents,
                storage_context=storage_context,
            )
            logging.info(f"Created new index for {pdf_file.name}")
            return index.as_query_engine()

def main():
    st.title("PDF Chat Bot")
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize session state for query engine
    if "query_engine" not in st.session_state:
        st.session_state.query_engine = None
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'])
    
    if uploaded_file is not None and st.session_state.query_engine is None:
        with st.spinner("Processing PDF..."):
            st.session_state.query_engine = process_pdf(uploaded_file)
        st.success("PDF processed successfully!")
    
    # Chat interface
    if st.session_state.query_engine is not None:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your PDF"):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.query_engine.query(prompt)
                    st.write(response.response)
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": str(response.response)})
    else:
        st.info("Please upload a PDF file to start chatting!")

if __name__ == "__main__":
    main() 