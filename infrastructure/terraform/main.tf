terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Configure these values for your environment
    # bucket         = "smartresolve-terraform-state-${aws_account_id}"
    # key            = "smartresolve/terraform.tfstate"
    # region         = "us-east-1"
    # encrypt        = true
    # dynamodb_table = "smartresolve-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "SmartResolve"
      Environment = var.environment
      ManagedBy   = "Terraform"
      CreatedAt   = timestamp()
    }
  }
}

# DynamoDB Tables
resource "aws_dynamodb_table" "summaries" {
  name           = "smartresolve-summaries-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "complaintId"
    type = "S"
  }

  attribute {
    name = "createdAt"
    type = "S"
  }

  global_secondary_index {
    name            = "complaintId-createdAt-index"
    hash_key        = "complaintId"
    range_key       = "createdAt"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  stream_specification {
    stream_view_type = "NEW_AND_OLD_IMAGES"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  tags = {
    Name = "smartresolve-summaries"
  }
}

resource "aws_dynamodb_table" "complaints" {
  name           = "smartresolve-complaints-${var.environment}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "customerId"
    type = "S"
  }

  attribute {
    name = "createdAt"
    type = "S"
  }

  global_secondary_index {
    name            = "customerId-createdAt-index"
    hash_key        = "customerId"
    range_key       = "createdAt"
    projection_type = "ALL"
  }

  stream_specification {
    stream_view_type = "NEW_AND_OLD_IMAGES"
  }

  point_in_time_recovery {
    enabled = var.environment == "prod"
  }

  tags = {
    Name = "smartresolve-complaints"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "storage" {
  bucket = "smartresolve-storage-${data.aws_caller_identity.current.account_id}-${var.environment}"

  tags = {
    Name = "smartresolve-storage"
  }
}

resource "aws_s3_bucket_versioning" "storage" {
  bucket = aws_s3_bucket.storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "storage" {
  bucket = aws_s3_bucket.storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.master.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "storage" {
  bucket = aws_s3_bucket.storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# SQS Queues
resource "aws_sqs_queue" "summarization" {
  name                      = "smartresolve-summarization-${var.environment}"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 1209600

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.summarization_dlq.arn
    maxReceiveCount     = 3
  })

  tags = {
    Name = "smartresolve-summarization-queue"
  }
}

resource "aws_sqs_queue" "summarization_dlq" {
  name                     = "smartresolve-summarization-dlq-${var.environment}"
  message_retention_seconds = 1209600

  tags = {
    Name = "smartresolve-summarization-dlq"
  }
}

# SNS Topics
resource "aws_sns_topic" "complaint_created" {
  name = "smartresolve-complaint-created-${var.environment}"

  tags = {
    Name = "smartresolve-complaint-created"
  }
}

resource "aws_sns_topic" "resolution_ready" {
  name = "smartresolve-resolution-ready-${var.environment}"

  tags = {
    Name = "smartresolve-resolution-ready"
  }
}

# KMS Key
resource "aws_kms_key" "master" {
  description             = "SmartResolve Master Encryption Key"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = {
    Name = "smartresolve-master-key"
  }
}

resource "aws_kms_alias" "master" {
  name          = "alias/smartresolve-${var.environment}"
  target_key_id = aws_kms_key.master.key_id
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "application" {
  name              = "/smartresolve/${var.environment}/application"
  retention_in_days = 30

  tags = {
    Name = "smartresolve-logs"
  }
}

# Data sources
data "aws_caller_identity" "current" {}

output "summaries_table_name" {
  value = aws_dynamodb_table.summaries.name
}

output "complaints_table_name" {
  value = aws_dynamodb_table.complaints.name
}

output "storage_bucket_name" {
  value = aws_s3_bucket.storage.id
}

output "summarization_queue_url" {
  value = aws_sqs_queue.summarization.id
}

output "kms_key_id" {
  value = aws_kms_key.master.arn
}
