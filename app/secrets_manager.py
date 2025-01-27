import json
import boto3

secrets_client = boto3.client("secretsmanager")

def get_secret(secret_name):
    """Retrieve OpenAI API Key from Secrets Manager"""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret[secret_name]
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None