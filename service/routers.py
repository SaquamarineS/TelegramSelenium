import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException

from service.models import MessageRequest
from telegram_robot import config
from telegram_robot.util import TelegramWeb

router = APIRouter()


@router.post("/send-message/")
async def send_message(request: MessageRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_message, request.usernames, request.message)
    return {
        "status": "В процессе",
        "message": f"Сообщение отправленно на {request.usernames}"
    }

def process_message(usernames: str, message: str):
    telegram = TelegramWeb()
    try:
        usernames = usernames.split(',')
        with telegram.authorization() as driver:
            for username in usernames:
                telegram.open_chat(driver, username.strip())
                telegram.send_message(driver, message)
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Отправка не удалась: {str(e)}")
