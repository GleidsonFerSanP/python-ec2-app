import os
import logging
from data_processing import generate_embeddings

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate(text):
    try:
        logger.info("Generate embeddings invoked", text)
        logger.debug("Processing text: %s", text)
        
        # Generate embedding for the text
        embeddings = generate_embeddings(text)
        
        if embeddings is None:
            logger.error("Failed to generate embeddings for the text")
            return None
        
        logger.info("Successfully generated %s embeddings", len(embeddings))
        
        # Return the embedding
        return embeddings
    except Exception as e:
        logger.error("An error occurred while generating embedding: %s", str(e), exc_info=True)
        raise