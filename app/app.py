import os
import logging
from flask import Flask, request, jsonify
from create_chunks import create
from generate_embeddings import generate
from store_embeddings import store, find_documents, delete_documents
from open_ai import generate_answer_with_context

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)

@app.route("/rag-api/embeddings", methods=["POST"])
def handle_request():
    try:
        logger.info("Received a request to process document.")
        
        # Get the request payload
        data = request.json
        if not data:
            logger.error("No JSON payload provided in the request.")
            return jsonify({"error": "No JSON payload provided"}), 400
        
        document_key = data.get("document_key")
        if not document_key:
            logger.error("No document_key provided in the request payload.")
            return jsonify({"error": "No document_key provided"}), 400
        
        logger.info(f"Processing document with key: {document_key}")
        
        # Create chunks from the document
        chunks = create(document_key)
        logger.info(f"Generated {len(chunks)} chunks from document with key: {document_key}")
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i + 1}/{len(chunks)}: {chunk[:50]}...")  # Log first 50 characters of the chunk
            embeddings = generate(chunk)
            logger.info(f"Generated embedding for chunk {i + 1}/{len(chunks)}.")
            store(chunk, embeddings, document_key, i)
            logger.info(f"Stored embedding for chunk {i + 1}/{len(chunks)}.")
        
        response = {"message": f"Document with key '{document_key}' processed successfully."}
        logger.info(f"Successfully processed document with key: {document_key}")
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"An error occurred while processing the request: {str(e)}", exc_info=True)
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route("/rag-api/embeddings", methods=["DELETE"])
def delete_embeddings():
    try:
        logger.info("Received a request to process document.")
        
        # Get the request payload
        data = request.json
        if not data:
            logger.error("No JSON payload provided in the request.")
            return jsonify({"error": "No JSON payload provided"}), 400
        
        namespace = data.get("namespace")
        if not namespace:
            logger.error("No namespace provided in the request payload.")
            return jsonify({"error": "No namespace provided"}), 400
        
        logger.info(f"Processing delete embeddings with namespace: {namespace}")
        
        delete_documents(namespace)
        
        response = {"message": f"Document with namespace '{namespace}' deleted successfully."}
        logger.info(f"Successfully deleted embeddings with namespace: {namespace}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"An error occurred while processing the request: {str(e)}", exc_info=True)
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/rag-api/query', methods=['POST'])
def query():
    """Performs RAG by retrieving relevant documents and generating a response."""
    data = request.json
    query_text = data.get("query")
    subject = data.get("subject")

    if not query_text or not subject:
        return jsonify({"error": "Query text and subject is required"}), 400

    query_embedding = generate(query_text)

    retrieved_docs = find_documents(query_embedding, subject)

    answer = generate_answer_with_context(retrieved_docs, query_text)

    return jsonify({"answer": answer, "retrieved_docs": retrieved_docs})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting Flask app on port {port}.")
    app.run(host="0.0.0.0", port=port, debug=True)
