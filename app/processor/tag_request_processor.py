import logging
import app.repository.post as post_repository
from app.service import ai_service


def process(message):
	logging.debug("Processing message: %s", message)
	post_id = message
	# Fetch the post from the database
	post = post_repository.find_post(post_id)
	if post is None:
		logging.error("Post not found: %s", post_id)
		return
	
	# Process the post
	tags = ai_service.tag_content(post.content)
	if len(tags) == 0:
		logging.error("No tags found for post: %s", post_id)
		return

	# Add the tags to the post
	post.tags = tags
	post_repository.update_post(post)
	logging.debug("Tags added to post: %s", post_id)
