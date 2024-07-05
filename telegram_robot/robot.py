import logging

from telegram_robot import util


def process_message(username: str, message: str) -> bool:
    """
    Прогоняем по всем процессам для входа в Telegram

    :param username: str
    :param message: str
    :return: bool
    """
    processed = False
    telegram = util.TelegramWeb()
    try:
        with telegram.authorization() as driver:
            telegram.open_chat(driver, username)
            telegram.send_message(driver, message)
            processed = True
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {str(e)}")
    return processed
