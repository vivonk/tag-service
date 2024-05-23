from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
	post_id: str
	content: str
	tags: Optional[list] = []
