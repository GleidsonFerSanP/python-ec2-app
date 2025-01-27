
# Create a security group for EC2 to allow HTTP & SSH access
resource "aws_security_group" "web_sg" {
  name        = "python_app_sg"
  description = "Allow HTTP and SSH"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH access (restrict in production)
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow HTTP access
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "python_app" {
  ami                    = "ami-0ac4dfaf1c5c0cce9"  # Ubuntu 22.04 Free-tier
  instance_type          = "t2.micro"
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = "my-new-key"  # Replace with your AWS SSH key
  associate_public_ip_address = true

  # User data script to install dependencies and run app
  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system
    sudo apt update -y

    # Install required packages
    sudo apt install -y nginx python3 python3-pip git

    # Clone the Flask App from GitHub
    sudo rm -rf /opt/flask_app
    sudo git clone https://github.com/GleidsonFerSanP/python-ec2-app.git /opt/flask_app

    # Install Flask dependencies
    sudo pip3 install -r /opt/flask_app/requirements.txt

    # Create Nginx Configuration
    cat <<'NGINX_CONF' | sudo tee /etc/nginx/sites-available/flask_app
    server {
        listen 80;
        server_name _;

        location /rag/ {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        error_page 502 503 504 /error.html;
    }
    NGINX_CONF

    # Enable the new Nginx configuration
    sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo systemctl restart nginx

    # Create a systemd service for Flask using Gunicorn
    cat <<'SERVICE' | sudo tee /etc/systemd/system/flask_app.service
    [Unit]
    Description=Flask Application
    After=network.target

    [Service]
    User=root
    WorkingDirectory=/opt/flask_app
    ExecStart=/usr/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 app:app
    Restart=always

    [Install]
    WantedBy=multi-user.target
    SERVICE

    # Start Flask on boot
    sudo systemctl daemon-reload
    sudo systemctl enable flask_app
    sudo systemctl start flask_app

    echo "Setup complete!"
  EOF

  tags = {
    Name = "PythonAppEC2"
  }
}

# Output the EC2 Public IP
output "ec2_public_ip" {
  value = aws_instance.python_app.public_ip
}
