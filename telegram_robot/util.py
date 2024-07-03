from contextlib import contextmanager
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

from telegram_robot import config


class CustomGoogle:
    def __init__(self):
        self.chrome_service = Service()

    @contextmanager
    def get_driver(self) -> webdriver.Chrome:
        driver = None
        try:
            driver = webdriver.Chrome(service=self.chrome_service)
            yield driver
        finally:
            driver.quit()

    def get_url(self, driver: Optional[webdriver.Chrome], url: str) -> None:
        if any([
            driver is None,
            not isinstance(driver, webdriver.Chrome)
        ]):
            driver = self.get_driver()
        driver.get(url)
        driver.maximize_window()


class TelegramWeb(CustomGoogle):
    def __init__(self):
        super().__init__()
        self.driver = None

    @contextmanager
    def authorization(self, url: str = config.Telegram.url):
        with self.get_driver() as driver:
            driver.get(url=url)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, config.Locators.qr_image))
            )
            WebDriverWait(driver, 100).until(
                EC.staleness_of(element=element)
            )
            yield driver

    @staticmethod
    def open_chat(driver: webdriver.Chrome, to_username: str) -> None:
        driver.find_element(By.XPATH, config.Locators.search).clear()
        driver.find_element(By.XPATH, config.Locators.search).send_keys(to_username)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config.Locators.chats))
        )
        chats = driver.find_elements(By.XPATH, config.Locators.chats)
        for chat in chats:
            try:
                chat.click()
                break
            except ElementNotInteractableException:
                pass

    @staticmethod
    def send_message(driver: webdriver.Chrome, message: str) -> None:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, config.Locators.input_message))
            )
        except TimeoutException:
            driver.find_elements(By.XPATH, config.Locators.chats)[0].click()
        input_message_element = driver.find_elements(By.XPATH, config.Locators.input_message)[0]
        input_message_element.send_keys(message)
        input_message_element.send_keys(Keys.RETURN)
