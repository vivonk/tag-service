import app.repository.post as post_repository
from app.service import ai_service
from loguru import logger

logger = logger.bind(name="tag_request_processor")

def process(message):
	logger.debug("Processing message: %s", message)
	post_id = message
	# Fetch the post from the database
	post = post_repository.find_post(post_id)
	if post is None:
		logger.error("Post not found: %s", post_id)
		return
	
	# Process the post
	tags = ai_service.tag_content(post.content)
	if len(tags) == 0:
		logger.error("No tags found for post: %s", post_id)
		return

	# Add the tags to the post
	post.tags = tags
	post_repository.update_post(post)
	logger.debug("Tags added to post: %s", post_id)
