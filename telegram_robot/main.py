from telegram_robot import util
from telegram_robot import config


def main():
    telegram = util.TelegramWeb()
    with telegram.authorization() as driver:
        for username, message in config.users.items():
            telegram.open_chat(driver=driver, to_username=username)
            telegram.send_message(driver=driver, message=message)
            driver.get(config.Telegram.url)


if __name__ == '__main__':
    main()
