import boto3
from botocore.exceptions import ClientError
import logging

from app.config import aws_account_id

sqs = boto3.client('sqs')


def add_message(message: str, queue_name: str):
	try:
		response = sqs.send_message(
			QueueUrl=get_queue_url(queue_name),
			MessageBody=message
		)
		return 'MessageId' in response
	except ClientError as e:
		logging.error(e)
		return False


def get_queue_url(queue_name: str):
	try:
		response = sqs.get_queue_url(
			QueueName=queue_name,
			QueueOwnerAWSAccountId=aws_account_id
		)
		return response['QueueUrl']
	except ClientError as e:
		if match_error(e, 'NonExistentQueue'):
			logging.error(f"Queue with name {queue_name} does not exist")
			raise e
		logging.error("Error occurred while fetching queue url")
		raise e


def match_error(error: ClientError, error_type: str):
	if error.response['Error']['Code'] == error_type:
		return True
