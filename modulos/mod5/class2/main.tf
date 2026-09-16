provider "aws" {
  region = "us-east-1"
}

# Key Pair para que Ansible pueda conectarse por SSH
resource "aws_key_pair" "deployer" {
  key_name   = "demo-hibrida-key"
  public_key = file(pathexpand("~/.ssh/id_rsa.pub"))
}

# Security Group: Permite HTTP (80) y SSH (22)
resource "aws_security_group" "ec2_sg" {
  name        = "demo-hibrida-sg"
  description = "Permite acceso HTTP y SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Instancia EC2
resource "aws_instance" "app_aws" {
  ami           = "ami-007dd4cdc89d5d91d" # Amazon Linux 2023 en us-east-1
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name           = "EC2-App-Hibrida"
    CentroDeCostos = "IT-500"
  }
}

output "ec2_public_ip" {
  value = aws_instance.app_aws.public_ip
}