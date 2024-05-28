import time
from decimal import Decimal

import app.repository.post as post_repository
from app.service import ai_service
from loguru import logger

logger = logger.bind(name="tag_request_processor")

def process(message):
	logger.debug("Processing message: {0}", message)
	post_id = message
	# Fetch the post from the database
	post = post_repository.find_post(post_id)
	if post is None:
		logger.error("Post not found: {0}", post_id)
		return
	
	# Process the post
	tags = ai_service.tag_content(post.content)
	if len(tags) == 0:
		logger.error("No tags applicable for post: {0}", post_id)
		return
	post.updated_time = Decimal(time.time())
	# Add the tags to the post
	post.tags = tags
	post_repository.update_post(post)
	logger.debug("Tags added to post: {0}", post_id)
