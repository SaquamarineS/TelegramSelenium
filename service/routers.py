import logging

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from service.database import SessionLocal
from service.models import Message
from service.models import MessageRequest
from telegram_robot import robot

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Basic authentication setup
security = HTTPBasic()


# Endpoint for sending messages
@router.post("/send-message", response_model=dict)
def send_message(
        request: MessageRequest,
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> dict:
    # Authentication check (replace with your own logic)
    if not (credentials.username == "admin" and credentials.password == "adminpass"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    # Process message
    try:
        processed = robot.process_message(username=request.username, message=request.message)

        # Save message to database
        message_entry = Message(username=request.username, message=request.message, status="Sent")
        db.add(message_entry)
        db.commit()

        return {
            "status": processed,
            "message": f"Message sent to user: {request.username}"
        }
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing message",
        )
