provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-mlflow-bucket"
  acl    = "private"

  tags = {
    Name        = "Name"
    Environment = "Env"
  }
}
