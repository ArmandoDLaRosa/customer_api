# infra/terraform/main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"  # Use the latest stable version
    }
  }
}

provider "aws" {
  region                      = var.region
  access_key                  = var.access_key
  secret_key                  = var.secret_key         
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  s3_use_path_style           = true

  endpoints {
    s3         = "http://localstack:4566"
    dynamodb   = "http://localstack:4566"
    sts        = "http://localstack:4566"
    iam        = "http://localstack:4566"
  }
}

module "s3" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name
  tags        = var.tags
  environment = var.environment
}

#resource "aws_dynamodb_table" "terraform_locks" {
#  name         = var.dynamodb_table_name
#  billing_mode = "PAY_PER_REQUEST"
#  hash_key     = "LockID"

#  attribute {
#    name = "LockID"
#    type = "S"
#  }

#  tags = var.tags
#}
