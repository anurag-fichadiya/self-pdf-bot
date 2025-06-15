import logging
import sys
import os

import qdrant_client
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings

Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

from llama_index.llms.groq import Groq

Settings.llm = Groq(model="llama-3.3-70b-versatile")


def main():
    print("Hello from self-pdf-bot!")
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

    documents = SimpleDirectoryReader("./pdfs/").load_data()

    client = qdrant_client.QdrantClient(
        # you can use :memory: mode for fast and light-weight experiments,
        # it does not require to have Qdrant deployed anywhere
        # but requires qdrant-client >= 1.1.1
        # location=":memory:"
        # otherwise set Qdrant instance address with:
        # url="http://<host>:<port>"
        # otherwise set Qdrant instance with host and port:
        host="93e216cb-a347-405b-a0e7-bc8ca7911536.europe-west3-0.gcp.cloud.qdrant.io",
        port=6333,
        # set API KEY for Qdrant Cloud
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Ecc00PIKhWvJVdgVfW-H0zqvAQ_XKcSkmxfPSqc-jvg"
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
