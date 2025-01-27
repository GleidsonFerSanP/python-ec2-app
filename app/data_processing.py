import os
import logging
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load environment variables from .env file (only for local testing)
if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)

def generate_chunks(document_text):
    try:
        logger.info("Generating chunks from document text")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_text(document_text)
        logger.info(f"Generated {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"An error occurred while generating chunks: {str(e)}", exc_info=True)
        return []

def generate_embeddings(chunk):
    try:
        # Log the chunk as JSON
        logger.info("Generating embedding for a chunk: %s", json.dumps(chunk, indent=2))
        
        # Generate the embedding
        response = embeddings.embed_query(chunk)
        
        # Log the embedding as JSON
        logger.info("Generated embedding successfully: %s", json.dumps(response, indent=2))
        
        return response
    except Exception as e:
        logger.error("An error occurred while generating embedding: %s", str(e), exc_info=True)
        raise
