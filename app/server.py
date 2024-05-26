from fastapi import FastAPI
from app.model import tagging, post
from app.service import post as post_service
from app.init import init
import logging

app = FastAPI()


@app.post("/post/tag")
def tag_post(request: tagging.TaggingRequest):
	return post_service.add_post(request)


@app.get("/post/{post_id}", response_model=post.Post)
def get_post(post_id: str):
	return post_service.get_post(post_id)


# save the request in DB
# publish the request on kafka topic
# return positive response to user if both operations are successful


# Run the application using uvicorn
if __name__ == "__main__":
	logging.info("Starting up tag service")
	import uvicorn
	init()
	uvicorn.run(app, host="0.0.0.0", port=8000)
