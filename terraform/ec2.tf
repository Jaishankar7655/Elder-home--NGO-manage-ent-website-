resource "aws_key_pair" "deployer_key" {
  key_name   = "deployer"
  public_key = file("my-keys.pub")
}

resource "aws_default_vpc" "default" {
    tags = {
        Name = "default-vpc"
    }
}

resource "aws_security_group" "my_sg" {
    name        = "allow_ssh_http 2"
    description = "Allow SSH and HTTP traffic"
    vpc_id      = aws_default_vpc.default.id
    
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
    ingress {
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        Name = "allow_ssh_http"
    }
}

resource "aws_instance" "web_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.deployer_key.key_name
  vpc_security_group_ids      = [aws_security_group.my_sg.id]
  associate_public_ip_address = true

  tags = {
    Name = "WebServer"
  }

  root_block_device {
    volume_size = var.volume_size
    volume_type = "gp2"
  }


}