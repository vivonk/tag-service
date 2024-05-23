import logging

import boto3
from botocore.exceptions import ClientError

from app.exception.DbException import DbException

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')
dynamodb_resource = boto3.resource('dynamodb')


def add_item(obj: dict, table_name: str):
	table = dynamodb_resource.Table(table_name)
	try:
		response = table.put_item(
			Item={
				**obj
			}
		)
		return response
	except ClientError as e:
		logging.error(e)
		raise DbException(e.response)


def find_item(key: dict, table_name: str):
	table = dynamodb_resource.Table(table_name)
	try:
		response = table.get_item(
			Key=key
		)
		if 'Item' not in response:
			return None
		return response['Item']
	except ClientError as e:
		logging.error(e)
		if match_error(e, 'ResourceNotFoundException'):
			return None
		raise DbException(e.response)


def match_error(error: ClientError, error_type: str):
	if error.response['Error']['Code'] == error_type:
		return True
