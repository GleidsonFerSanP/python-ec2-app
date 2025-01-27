import logging
from vector_store import store_on_pinacone, find_on_pinacone, delete_on_pinacone, delete_on_pinacone_by_ids

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def store(chunk, embeddings, document_key, i):
    """
    Stores a chunk and its embeddings in Pinecone.

    Args:
        chunk (str): The chunk of text to store.
        embeddings (list): The embeddings associated with the chunk.
        document_key (str): The document key for identification.
        i (int): The index of the chunk.
    """
    try:
        logger.info("store() invoked with chunks size: %s, document_key: %s, index: %d", len(chunk), document_key, i)
        logger.debug("Embeddings: %s", len(embeddings))
        
        logger.info("Storing chunk and embedding in Pinecone")
        store_on_pinacone(chunk, embeddings, document_key, i)
        
        logger.info("Successfully stored chunk and embeddings in Pinecone")
    except Exception as e:
        logger.error("An error occurred while storing in Pinecone: %s", str(e), exc_info=True)
        raise

def find_documents(text_query, namespace):
    """
    Finds documents in Pinecone based on a text query.

    Args:
        text_query (str): The query text to search for.
    """
    try:
        logger.info("find_documents() invoked with text_query: %s", text_query)
        
        logger.info("Searching for documents in Pinecone")
        results = find_on_pinacone(text_query, namespace)
        
        logger.info("Successfully retrieved documents from Pinecone")
        logger.debug("Retrieved documents: %s", results)
        
        return results
    except Exception as e:
        logger.error("An error occurred while searching in Pinecone: %s", str(e), exc_info=True)
        raise

def delete_documents(namespace):
    try:
        logger.info("delete_documents() invoked with text_query: %s", namespace)
        
        delete_on_pinacone(namespace)
        
        logger.info("Successfully delete_documents documents on Pinecone")
    except Exception as e:
        logger.error("An error occurred while searching in Pinecone: %s", str(e), exc_info=True)
        raise