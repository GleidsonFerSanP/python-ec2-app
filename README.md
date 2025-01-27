deactivate  # Exit venv (if active)
rm -rf venv  # Delete venv (Linux/macOS)
rmdir /s /q venv  # Delete venv (Windows)
python -m venv venv  # Recreate virtual environment
source venv/bin/activate  # Activate venv (Linux/macOS)
venv\Scripts\activate  # Activate venv (Windows)


pip install --upgrade --no-cache-dir -r requirements.txt
