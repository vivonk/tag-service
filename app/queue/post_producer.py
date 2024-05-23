from app.model.post import Post
from app.queue import sqs
from app import config


def add_post(post: Post):
	return sqs.add_message(post.post_id, config.tag_request_queue)

