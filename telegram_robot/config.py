import os

from dotenv import find_dotenv, load_dotenv

env_file_ = find_dotenv(rf'assets\.env.{os.getenv("ENV", "development")}')
env_file = env_file_ if env_file_ else find_dotenv(f'.env.{os.getenv("ENV", "development")}')
load_dotenv(env_file)


class Locators:
    qr_image = '//canvas[@class="qr-canvas"]'
    search = '//input[@type="text"]'
    chats = '//div[@class="search-group__name"]/following-sibling::ul[@class="chatlist"]'
    input_message = '//div[@class="input-message-container"]//div'


class Telegram:
    url = os.getenv('TELEGRAM_URL', 'https://web.telegram.org/k/')


class MessageDB:
    user = os.getenv('DATABASE_USER')
    password = os.getenv('DATABASE_PASSWORD')
    db_name = os.getenv('DATABASE_NAME')
