"""CONSOLE APP"""
import logging
import sys
import os

import qdrant_client
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from llama_index.llms.groq import Groq

from config import *  # Import all configuration variables

# Initialize settings
Settings.embed_model = FastEmbedEmbedding(model_name=EMBEDDING_MODEL)
Settings.llm = Groq(model=LLM_MODEL)

# Initialize logging configuration to output to stdout with INFO level
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def main():
    print("Hello from self-pdf-bot!")
    
    documents = SimpleDirectoryReader("./pdfs/").load_data()
    
    # Initialize Qdrant client
    client = qdrant_client.QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY
    )

    vector_store = QdrantVectorStore(client=client, collection_name="budget_speech")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )

    query_engine = index.as_query_engine()
    
    while True:
        user_input = input("\nEnter your question (type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        response = query_engine.query(user_input)
        print("\n" + "="*50)
        print("Question:", user_input)
        print("-"*50)
        print("Answer:", response)
        print("="*50)

if __name__ == "__main__":
    main()
