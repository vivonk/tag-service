import os
import requests
import json
from loguru import logger

logger = logger.bind(name="ai_service")

ai_service_url = os.environ["AI_SERVICE_URL"]
model_name = os.environ["MODEL_NAME"]


def tag_content(content: str):
	response = make_request(content)
	response = response['response']
	response = json.loads(response)
	if 'tags' not in response:
		logger.error("No tags found for content")
		return []
	return response['tags']


def make_request(content):
	url = f"{ai_service_url}/api/generate"
	body = {
		"model": model_name,
		"prompt": content,
		"format": "json",
		"stream": False
	}
	response = requests.post(url, json=body, timeout=240)
	if response.status_code != 200:
		logger.error(f"Failed to tag content: {response.text}")
		raise Exception("Failed to tag content")
	return response.json()
