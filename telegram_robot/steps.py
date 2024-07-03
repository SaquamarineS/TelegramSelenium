from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from telegram_robot import config


def runner(number: int) -> None:
    webdriver.ChromeOptions()

    with webdriver.Chrome() as driver:
        # По ссылке переходить
        driver.get(config.Telegram.url)
        driver.maximize_window()

        # Ждать пока не зайдет
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config.Locators.qr_image))
        )
        WebDriverWait(driver, 100).until(
            EC.staleness_of(element=element)
        )

        # Поиск по имени
        driver.find_element(By.XPATH, config.Locators.search).clear()
        driver.find_element(By.XPATH, config.Locators.search).send_keys(config.Users.users_list[number])  # @waves0101
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, config.Locators.chats))
        )
        driver.find_elements(By.XPATH, config.Locators.chats)[0].click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config.Locators.input_message))
        )

        # Отправка сообщения
        input_message_element = driver.find_elements(By.XPATH, config.Locators.input_message)[0]
        input_message_element.send_keys(config.Users.text_list_per_user[number])
        input_message_element.send_keys(Keys.RETURN)

