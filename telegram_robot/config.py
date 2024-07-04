import os


class Locators:
    qr_image = '//canvas[@class="qr-canvas"]'
    search = '//input[@type="text"]'
    chats = '//div[@class="search-group__name"]/following-sibling::ul[@class="chatlist"]'
    input_message = '//div[@class="input-message-container"]//div'


class Telegram:
    url = os.getenv('TELEGRAM_URL')
