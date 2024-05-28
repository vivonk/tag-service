import decimal
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
	post_id: str
	content: str
	tags: Optional[list] = []
	added_time: Optional[Decimal] = None
	updated_time: Optional[Decimal] = None
