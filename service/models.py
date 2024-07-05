from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MessageRequest(BaseModel):
    username: str
    message: str


class Message(Base):
    __tablename__ = "message_logs"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    message = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.time)
