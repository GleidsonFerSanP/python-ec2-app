import os
from pinecone import Pinecone
import logging
from dotenv import load_dotenv

if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# PINECONE_API_KEY = get_secret(PINECONE_API_KEY_SECRET_NAME)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(name=PINECONE_INDEX)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def store_on_pinacone(chunk, embeddings, document_key, i):
    try:
        logger.info("store_on_pinacone invoked with chunk: %s and embeddings: %s", chunk, embeddings)
        
        # Store in Pinecone
        index.upsert(vectors=[
            {
            "id": f"{document_key}-{i}", 
            "values": embeddings,
            "metadata": {"subject": document_key, "text": chunk}
            },
        ],  namespace=document_key)
        
        logger.info("Successfully stored chunk and embeddings in Pinecone")
    except Exception as e:
        logger.error("An error occurred while storing in Pinecone: %s", str(e), exc_info=True)
        raise

def find_on_pinacone(query_embedding, namespace):
    try:
        logger.info("find_on_pinacone invoked with query_embedding: %s",query_embedding)
        
        # Search Pinecone for similar documents
        results = index.query(vector=query_embedding, namespace=namespace,  top_k=20, include_metadata=True, include_values=True)
        
        logger.info("Successfully fetched find_on_pinacone in Pinecone results %s", results)
        
        retrieved_docs = [match['metadata']['text'] for match in results['matches']]
        
        logger.info("Successfully fetched find_on_pinacone in Pinecone retrieved_docs %s", retrieved_docs)
        return retrieved_docs
    except Exception as e:
        logger.error("An error occurred while fething in Pinecone: %s", str(e), exc_info=True)
        raise

def delete_on_pinacone(namespace):
    try:
        logger.info("delete_on_pinacone invoked with namespace: %s",namespace)
        
        # Search Pinecone for similar documents
        
        response = index.delete(delete_all=True, namespace=namespace)
        
        logger.info("Successfully fetched delete_on_pinacone in Pinecone response %s", response)
    except Exception as e:
        logger.error("An error occurred while fething in Pinecone: %s", str(e), exc_info=True)
        raise

def delete_on_pinacone_by_ids(vector_ids):
    try:
        logger.info("delete_on_pinacone_by_ids invoked with vector_ids size: %s",len(vector_ids))
        
        response = index.delete(ids=vector_ids)
        
        logger.info("Successfully fetched delete_on_pinacone_by_ids in Pinecone response %s", response)
    except Exception as e:
        logger.error("An error occurred while fething in Pinecone: %s", str(e), exc_info=True)
        raise