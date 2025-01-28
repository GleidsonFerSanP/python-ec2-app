deactivate  # Exit venv (if active)
rm -rf venv  # Delete venv (Linux/macOS)
rmdir /s /q venv  # Delete venv (Windows)
python -m venv venv  # Recreate virtual environment
source venv/bin/activate  # Activate venv (Linux/macOS)
venv\Scripts\activate  # Activate venv (Windows)


pip install --upgrade --no-cache-dir -r requirements.txt

    curl -X POST 54.165.177.195:8080/rag/query \
-H "Content-Type: application/json" \
-d '{ "query": "faca um disclaimer sobre Jeanne Boyarsky ? responda em portugues", "subject": "rag-poc/OCP Oracle Certified Professional Java SE 8 Programmer II Study Guide Exam 1Z0-809.pdf"}'

    curl -X POST 52.3.240.174/rag/query \
-H "Content-Type: application/json" \
-d '{ "query": "faca um disclaimer sobre Jeanne Boyarsky ? responda em portugues", "subject": "rag-poc/OCP Oracle Certified Professional Java SE 8 Programmer II Study Guide Exam 1Z0-809.pdf"}'

    curl -X POST http://ec2-34-203-33-244.compute-1.amazonaws.com/rag-api/query \
-H "Content-Type: application/json" \
-d '{ "query": "faca um disclaimer sobre Jeanne Boyarsky ? responda em portugues", "subject": "rag-poc/OCP Oracle Certified Professional Java SE 8 Programmer II Study Guide Exam 1Z0-809.pdf"}'


curl --location 'http://127.0.0.1:8000/rag-api/query' \
--header 'Content-Type: application/json' \
--data '{
    "query": "faca um disclaimer sobre Jeanne Boyarsky ? responda em portugues",
    "subject": "rag-poc/OCP Oracle Certified Professional Java SE 8 Programmer II Study Guide Exam 1Z0-809.pdf"
}'