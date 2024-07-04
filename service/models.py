from pydantic import BaseModel
from typing import List

class MessageRequest(BaseModel):
    usernames: str
    message: str
