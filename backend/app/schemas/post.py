from typing import Literal
from pydantic import BaseModel,Field

class PostRequest(BaseModel):
    title : str = Field(min_length=1, max_length=100)
    content : str = Field(min_length=1)
    tags : list[str] = Field(default_factory=list, max_length=5)