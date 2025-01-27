
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
  ami                    = "ami-0ac4dfaf1c5c0cce9"
  instance_type          = "t2.micro"
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name 
  key_name               = "my-new-key"
  associate_public_ip_address = true

  # User data script to install dependencies and run app
  user_data = file("${path.module}/startup_python_ec2_app.sh")
  tags = {
    Name = "PythonAppEC2"
  }
}

# Output the EC2 Public IP
output "ec2_public_ip" {
  value = aws_instance.python_app.public_ip
}
