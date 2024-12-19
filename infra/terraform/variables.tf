# infra/terraform/variables.tf

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "local"
}
variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "access_key" {
  default = "test"
}

variable "secret_key" {
  default = "test"
}

variable "tags" {
  description = "Common tags for resources"
  type        = map(string)
  default = {
    Environment = "local"
    Project     = "CustomerAPI"
  }
}

variable "s3_bucket_name" {
  description = "S3 bucket name for data lake"
  type        = string
  default     = "local-datalake"
}

#variable "dynamodb_table_name" {
#  description = "DynamoDB table name for state locking"
#  type        = string
#  default     = "terraform-locks"
#}
