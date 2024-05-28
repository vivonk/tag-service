from app.exception.DbException import DbException
from app.exception.RepositoryException import RepositoryException
from app.repository import dynamodb
from app.model.post import Post
from loguru import logger

logger = logger.bind(name="post_repository")

table_name = "posts"
post_id_key = "post_id"
content_key = "content"
tags_key = "tags"
added_time_key = "added_time"
updated_time_key = "updated_time"
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
		tags_key: post.tags,
		added_time_key: post.added_time,
		updated_time_key: post.updated_time
	}
	try:
		logger.info(f"Adding post with id {post.post_id} to the database")
		return dynamodb.add_item(obj, table_name)
	except DbException:
		logger.error("Error while adding post to the database")
		raise RepositoryException("Error while adding post to the database")


def find_post(post_id: str):
	key = {
		post_id_key: post_id
	}
	try:
		logger.debug(f"Fetching post with id {post_id} from the database")
		value = dynamodb.find_item(key, table_name)
		if value is None:
			return None
		post = Post(post_id=value[post_id_key], content=value[content_key], tags=value[tags_key])
		if updated_time_key in value:
			post.updated_time = value[updated_time_key]
		if added_time_key in value:
			post.added_time = value[added_time_key]
		return post
	except DbException:
		logger.error("Error while fetching post from the database")
		raise RepositoryException("Error while adding post to the database")


def update_post(post: Post):
	obj = {
		post_id_key: post.post_id,
		content_key: post.content,
		tags_key: post.tags,
		added_time_key: post.added_time,
		updated_time_key: post.updated_time
	}
	try:
		logger.debug(f"Updating post with id {post.post_id} in the database")
		return dynamodb.add_item(obj, table_name)
	except DbException:
		logger.error("Error while updating post in the database")
		raise RepositoryException("Error while updating post in the database")
