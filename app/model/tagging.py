from pydantic import BaseModel


# Define the request and response model
class TaggingRequest(BaseModel):
	post_id: str
	content: str


class Response(BaseModel):
	success: bool
	message: str
	code: str
	