from app.exception.DbException import DbException
from app.exception.RepositoryException import RepositoryException
from app.repository import dynamodb
from app.model.post import Post

table_name = "posts"
post_id_key = "post_id"
content_key = "content"
tags_key = "tags"
key_schema = [{
	'AttributeName': post_id_key,
	'KeyType': 'HASH'
}]

attributes = [{
	'AttributeName': post_id_key,
	'AttributeType': 'S'
}]


def add_post(post: Post):
	obj = {
		post_id_key: post.post_id,
		content_key: post.content,
		tags_key: post.tags
	}
	try:
		return dynamodb.add_item(obj, table_name)
	except DbException:
		raise RepositoryException("Error while adding post to the database")


def find_post(post_id: str):
	key = {
		post_id_key: post_id
	}
	try:
		value = dynamodb.find_item(key, table_name)
		if value is None:
			return None
		return Post(post_id=value[post_id_key], content=value[content_key], tags=value[tags_key])
	except DbException:
		raise RepositoryException("Error while adding post to the database")


def update_post(post: Post):
	obj = {
		post_id_key: post.post_id,
		content_key: post.content,
		tags_key: post.tags
	}
	try:
		return dynamodb.add_item(obj, table_name)
	except DbException:
		raise RepositoryException("Error while updating post in the database")
