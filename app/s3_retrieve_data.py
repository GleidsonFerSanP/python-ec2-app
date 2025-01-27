import boto3
import os
import io
import csv
import pandas as pd
import PyPDF2
from docx import Document
from dotenv import load_dotenv

# Load environment variables from .env file (only for local testing)
if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv("S3_BUCKET")

def retrieve_data_from_s3(document_key):
    # Retrieve data from S3
    print(f"Retrieve,s3 document bucket {BUCKET_NAME} documentkey {document_key}")
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=document_key)
        print(f"Retrieved,s3 document response {response}")
        
        # Get the file extension
        file_extension = document_key.split('.')[-1].lower()
        raw_data = response['Body'].read()
        print(f"Retrieved,s3 document file_extension {file_extension}")
        if file_extension == 'pdf':
            # Handle PDF files
            b = io.BytesIO(raw_data)
            pdf_reader = PyPDF2.PdfReader(b)
            print(f"Retrieved,s3 document pdf_reader pages size {len(pdf_reader.pages)}")
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            
            print(f"Retrieved,s3 document pdf_text {pdf_text}")
            return pdf_text
        
        elif file_extension == 'txt':
            # Handle TXT files
            return raw_data.decode('utf-8')
        
        elif file_extension == 'docx':
            # Handle DOCX files
            doc = Document(io.BytesIO(raw_data))
            doc_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return doc_text
        
        elif file_extension == 'csv':
            # Handle CSV files
            csv_data = raw_data.decode('utf-8')
            csv_reader = csv.reader(io.StringIO(csv_data))
            csv_content = [row for row in csv_reader]
            return csv_content
        
        elif file_extension == 'xlsx':
            # Handle XLSX files
            excel_data = pd.read_excel(io.BytesIO(raw_data))
            return excel_data.to_dict(orient='records')  # Convert to a list of dictionaries
        
        elif file_extension == 'md':
            # Handle Markdown files
            return raw_data.decode('utf-8')
        
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    except Exception as e:
        print(f"Error retrieving data from S3: {e}")
        return None
