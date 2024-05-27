from fastapi import FastAPI
from app.model import tagging, post
from app.service import post as post_service
from app.init import init

from loguru import logger

app = FastAPI()

logger = logger.bind(name="app")


@app.on_event("startup")
async def startup_event():
	init()
	logger.info("Starting up the application")


@app.post("/post/tag")
async def tag_post(request: tagging.TaggingRequest):
	return post_service.add_post(request)


@app.get("/post/{post_id}", response_model=post.Post)
async def get_post(post_id: str):
	return post_service.get_post(post_id)
