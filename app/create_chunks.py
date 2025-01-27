import boto3
import logging
from s3_retrieve_data import retrieve_data_from_s3
from data_processing import generate_chunks

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def create(document_key):
    logger.info("create chunks invoked with document_key: %s", document_key)

    # Retrieve the document text from S3
    document_text = retrieve_data_from_s3(document_key)
    if not document_text:
        logger.error("Failed to retrieve document text for key: %s", document_key)
        return {
            "statusCode": 500,
            "body": "Failed to retrieve document text"
        }
    logger.info("Successfully retrieved document text for key: %s", document_key)

    # Generate chunks from the document text
    chunks = generate_chunks(document_text)
    logger.info("Generated %d chunks from document text", len(chunks))

    # Return the response
    return chunks