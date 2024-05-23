# Create an SQS queue
resource "aws_sqs_queue" "tag-request-queue" {
  name                      = "tag-request-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.tag-request-dlq.arn
    maxReceiveCount     = 4
  })
}


# Create a dead letter queue for the main queue
resource "aws_sqs_queue" "tag-request-dlq" {
  name = "tag-request-dlq"
}