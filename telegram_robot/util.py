import logging
from contextlib import contextmanager
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from telegram_robot import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CustomGoogle:
    def __init__(self):
        self.chrome_service = Service()

    @contextmanager
    def get_driver(self) -> webdriver.Chrome:
        driver = None
        try:
            logger.info("Начало Chrome WebDriver")
            driver = webdriver.Chrome(service=self.chrome_service)
            yield driver
        finally:
            if driver:
                logger.info("Закрытие Chrome WebDriver")
                driver.quit()

    def get_url(self, driver: Optional[webdriver.Chrome], url: str) -> None:
        if any([
            driver is None,
            not isinstance(driver, webdriver.Chrome)
        ]):
            driver = self.get_driver()
        logger.info(f"Навигация по URL: {url}")
        driver.get(url)
        driver.maximize_window()


class TelegramWeb(CustomGoogle):
    def __init__(self):
        super().__init__()
        self.driver = None

    @contextmanager
    def authorization(self, url: str = config.Telegram.url) -> object:
        with self.get_driver() as driver:
            try:
                if not isinstance(url, str):
                    raise ValueError("URL должен быть строкой.")
                logger.info(f"Авторизация по URL: {url}")
                driver.get(url=url)
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, config.Locators.qr_image))
                )
                WebDriverWait(driver, 100).until(
                    EC.staleness_of(element=element)
                )
                yield driver
            except Exception as e:
                logger.error(f"Авторизация провалена: {str(e)}")
                raise e

    @staticmethod
    def open_chat(driver: webdriver.Chrome, to_username: str) -> None:
        try:
            logger.info(f"Открытие чата: {to_username}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, config.Locators.search))
            )
            driver.find_element(By.XPATH, config.Locators.search).clear()
            driver.find_element(By.XPATH, config.Locators.search).send_keys(to_username)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, config.Locators.chats))
            )
            chats = driver.find_elements(By.XPATH, config.Locators.chats)
            for chat in chats:
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable(chat)
                    ).click()
                    logger.info(f"Открытие чата по Username: {to_username}")
                    break
                except ElementNotInteractableException:
                    pass
        except TimeoutException:
            logger.error(f"Тайм-аут при открытии чата с именем пользователя: {to_username}")
            raise

    @staticmethod
    def send_message(driver: webdriver.Chrome, message: str) -> None:
        try:
            logger.info(f"ОТправка сообщения: {message}")
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, config.Locators.input_message))
            )
        except TimeoutException:
            logger.warning("Элемент входного сообщения найден не сразу")
            driver.find_elements(By.XPATH, config.Locators.chats)[0].click()
        input_message_element = driver.find_elements(By.XPATH, config.Locators.input_message)[0]
        input_message_element.send_keys(message)
        input_message_element.send_keys(Keys.RETURN)
        logger.info("Сообщение отправлено успешно")
