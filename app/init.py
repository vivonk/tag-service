# create dynamo db tables if not exist
from loguru import logger

from app.repository.dynamodb import dynamodb
from app.repository.post import table_name as post_table_name, key_schema, attributes

logger = logger.bind(name="init")

def init_dynamo_db():
	logger.info("Initializing DynamoDB tables...")
	response = dynamodb.list_tables()
	if post_table_name not in response["TableNames"]:
		dynamodb.create_table(TableName=post_table_name, KeySchema=key_schema, AttributeDefinitions=attributes,
		                      BillingMode='PAY_PER_REQUEST')


def init():
	logger.info("Initializing the application...")
	init_dynamo_db()
