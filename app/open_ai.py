import openai
import os
import logging
from dotenv import load_dotenv

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load environment variables from .env file (only for local testing)
if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_answer_with_context(retrieved_docs, query_text):
    """
    Builds context from retrieved documents and generates an answer using OpenAI GPT.

    Args:
        retrieved_docs (list): List of retrieved documents.
        query_text (str): The query text for which the answer is to be generated.

    Returns:
        str: The generated answer.
    """
    try:
        # Build context for OpenAI completion
        # Build context for OpenAI completion
        context = "\n".join(retrieved_docs)
        prompt = f"Context: {context}\n\nQuestion: {query_text}\nAnswer:"

        # Generate answer using OpenAI GPT
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}]
        )

        answer = completion.choices[0].message.content

        return answer
    except Exception as e:
        logger.error(f"An error occurred while generating the answer: {str(e)}", exc_info=True)
        raise