# infra/terraform/outputs.tf

output "s3_bucket_name" {
  value = module.s3.bucket_name
}

#output "dynamodb_table_name" {
#  value = aws_dynamodb_table.terraform_locks.name
#}
