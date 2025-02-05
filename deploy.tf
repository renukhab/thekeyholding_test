provider "aws" {
  region = "us-east-1"  # Change this to your preferred AWS region
}

resource "aws_vpc" "interstellar_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.interstellar_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"
}

resource "aws_security_group" "flask_sg" {
  vpc_id = aws_vpc.interstellar_vpc.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
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

resource "aws_instance" "flask_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # Change this to your preferred AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public_subnet.id
  security_groups = [aws_security_group.flask_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y python3 python3-pip
              pip3 install flask flask-restx flask-sqlalchemy psycopg2
              cd /home/ubuntu
              git clone https://github.com/your-repo/interstellar-api.git
              cd interstellar-api
              FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
              EOF

  tags = {
    Name = "Flask-API-Server"
  }
}

resource "aws_db_instance" "postgres_db" {
  identifier           = "interstellar-db"
  engine              = "postgres"
  engine_version      = "13"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  storage_type        = "gp2"
  username           = "admin"
  password           = "password"
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.flask_sg.id]
  skip_final_snapshot = true
}

output "instance_ip" {
  value = aws_instance.flask_server.public_ip
}

output "db_endpoint" {
  value = aws_db_instance.postgres_db.endpoint
}
