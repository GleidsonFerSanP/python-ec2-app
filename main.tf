
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
  ami                    = "ami-0c55b159cbfafe1f0"  # Ubuntu 22.04 Free-tier
  instance_type          = "t2.micro"
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  key_name               = "my-key"  # Replace with your AWS SSH key
  associate_public_ip_address = true

  # User data script to install dependencies and run app
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y python3 python3-pip unzip

              # Download app from S3 or GitHub (if applicable)
              # Example: Uncomment if using GitHub
              git clone https://github.com/GleidsonFerSanP/python-ec2-app.git /home/ubuntu/app

              # Copy your local app folder (OPTION 2: Manually upload it after EC2 creation)
              # mkdir -p /home/ubuntu/app

              # Install dependencies
              if [ -f "/home/ubuntu/app/requirements.txt" ]; then
                  pip install -r /home/ubuntu/app/requirements.txt
              fi

              # Run the Flask app (assuming app.py is in the root of 'app' folder)
              nohup python3 /home/ubuntu/app/app.py > /home/ubuntu/app.log 2>&1 &
              EOF

  tags = {
    Name = "PythonAppEC2"
  }
}

# Output the EC2 Public IP
output "ec2_public_ip" {
  value = aws_instance.python_app.public_ip
}
