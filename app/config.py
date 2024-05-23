import os

tag_request_queue = os.environ["QUEUE_NAME"]
tag_request_dlq = os.environ["DLQ_NAME"]
aws_account_id = os.environ["AWS_ACCOUNT_ID"]
ai_service_url = os.environ["AI_SERVICE_URL"]
