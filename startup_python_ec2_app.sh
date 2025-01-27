#!/bin/bash

# Exit on any error
set -e

# Update system packages
sudo yum update -y

# Install required dependencies
sudo yum install -y git python3 python3-pip nginx

# Clone the GitHub repository
cd /home/ec2-user
git clone https://github.com/GleidsonFerSanP/python-ec2-app.git
cd python-ec2-app

# Install Supervisor using pip (since it's missing from Amazon Linux 2023)
pip install --upgrade pip
pip install supervisor

# Create and activate virtual environment
python3 -m venv /home/ec2-user/python-ec2-app/app/venv
source /home/ec2-user/python-ec2-app/app/venv/bin/activate

# Install Python dependencies
pip install -r app/requirements.txt gunicorn

# Set environment variables
export FLASK_APP=app/app.py
export FLASK_ENV=production

# ✅ Create Supervisor config file
sudo tee /etc/supervisord.conf > /dev/null <<EOF
[supervisord]
logfile=/var/log/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/var/run/supervisord.pid
nodaemon=false

[unix_http_server]
file=/var/run/supervisor.sock
chmod=0700

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock

[program:python-app]
command=/home/ec2-user/python-ec2-app/app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app.app:app
directory=/home/ec2-user/python-ec2-app/app
autostart=true
autorestart=true
stderr_logfile=/var/log/python-app.err.log
stdout_logfile=/var/log/python-app.out.log
EOF

# ✅ Start Supervisor
supervisord -c /etc/supervisord.conf

# ✅ Ensure application is started
supervisorctl reread
supervisorctl update
supervisorctl start python-app

# Configure Nginx
sudo tee /etc/nginx/conf.d/python-ec2-app.conf > /dev/null <<EOF
server {
    listen 80;

    location /rag-api/embeddings {
        proxy_pass http://127.0.0.1:8000/rag-api/embeddings;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /rag-api/query {
        proxy_pass http://127.0.0.1:8000/rag-api/query;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Restart Nginx to apply changes
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "Deployment complete! API is running on port 80 via Nginx with Gunicorn & Supervisor."
