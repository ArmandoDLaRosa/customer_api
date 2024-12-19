variable "environment" {
  description = "The environment where resources are deployed (e.g., dev, prod)"
  type        = string
}
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}
