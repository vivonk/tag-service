from fastapi import Response, HTTPException, status

from app.exception.RepositoryException import RepositoryException
from app.model.tagging import TaggingRequest
import app.model.post as post
from app.repository import post as post_repo
from app.queue import post_producer
import urllib3
urllib3.disable_warnings()
from loguru import logger


logger = logger.bind(name="post_service")

"""
This function is used to add a post to the database and alongside add the same tag request to the kafka topic
"""

def add_post(request: TaggingRequest):
	new_post = post.Post(post_id=request.post_id, content=request.content)
	try:
		value = find_post(new_post.post_id)
		if value is not None:
			logger.error(f"Post with id {new_post.post_id} already exists")
			raise HTTPException(status_code=400, detail="Post already exists")
		post_repo.add_post(new_post)
		message_sent = post_producer.add_post(new_post)
		if message_sent:
			logger.info(f"Post with id {new_post.post_id} added to the database and sent for tagging")
			return Response(status_code=status.HTTP_201_CREATED)
		raise HTTPException(status_code=500, detail="Unable to accept posts for tagging. Please try again later.")
	except RepositoryException:
		logger.error("Error while adding post to the database")
		raise HTTPException(status_code=500, detail="Unable to accept posts for tagging. Please try again later.")


def find_post(post_id: str):
	try:
		logger.info(f"Fetching post with id {post_id} from the database")
		value = post_repo.find_post(post_id)
		return value
	except RepositoryException:
		logger.error("Error while fetching post from the database")
		raise HTTPException(status_code=500, detail="Unable to find posts right now. Please try again later.")


def get_post(post_id: str):
	value = find_post(post_id)
	if value is None:
		logger.error(f"Post with id {post_id} not found")
		raise HTTPException(status_code=404, detail="Post not found")
	return value
