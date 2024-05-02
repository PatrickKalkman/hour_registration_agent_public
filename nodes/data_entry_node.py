import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp
from loguru import logger

# Constants
DEFAULT_WAIT_TIME = 10


def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(DEFAULT_WAIT_TIME)
    logger.info("WebDriver has been initialized.")
    return driver


def login(driver):
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    LOGIN_URL = os.getenv('LOGIN_URL')
    logger.info("Opening login page...")
    driver.get(LOGIN_URL)
    time.sleep(2)  # Ensuring the page fully loads
    email_element = driver.find_element(By.ID, 'email')
    email_element.send_keys(EMAIL)
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="button"]').click()
    logger.info("Login attempted with provided credentials.")
    time.sleep(2)  # Allow time for potential redirects


def enter_totp_code(driver):
    TOTP_SECRET = os.getenv('TOTP_SECRET')
    logger.info("Entering TOTP code...")
    totp = pyotp.TOTP(TOTP_SECRET)
    WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, 'code'))).send_keys(totp.now())
    driver.find_element(By.CSS_SELECTOR, 'button[data-testid="button"]').click()
    logger.info("TOTP code entered and submitted.")
    time.sleep(2)  # Wait for any post-OTP submission processing


def navigate_to_time_entry_page(driver):
    BASE_TIME_ENTRY_URL = os.getenv('BASE_TIME_ENTRY_URL')
    date = datetime.now().strftime('%Y-%m-%d')
    url = f"{BASE_TIME_ENTRY_URL}?date={date}"
    driver.get(url)
    logger.info(f"Navigation to time entry page for date {date}.")
    time.sleep(2)  # Ensure the page and all scripts have loaded


def enter_time_details(driver, customer_name, description):
    logger.info("Entering time and description...")
    WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
        EC.visibility_of_element_located((By.ID, 'time'))).send_keys('8')
    select_project(driver, customer_name)
    select_dropdown_option(driver, 'taskId', 0)
    driver.find_element(By.ID, 'description').send_keys(description)
    driver.find_element(By.XPATH, "//button[contains(.,'Toevoegen')]").click()
    logger.info("Time entry submitted successfully.")


def select_project(driver, project):
    customer = os.getenv("CUSTOMER1")
    project_id = {customer: 2, 'default': 1}.get(project, 1)
    select_dropdown_option(driver, 'projectId', project_id)


def select_dropdown_option(driver, element_id, option_index):
    dropdown = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, element_id)))
    dropdown.click()
    options = WebDriverWait(driver, DEFAULT_WAIT_TIME).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".react-select__option")))
    options[option_index].click()
    logger.info(f"Option {option_index} selected from {element_id}.")


def data_entry_node(state):
    driver = setup_driver()
    try:
        customer = state["customer_name"]
        description = state["registration_description"]
        login(driver)
        enter_totp_code(driver)
        navigate_to_time_entry_page(driver)
        enter_time_details(driver, customer, description)
    except Exception as e:
        logger.exception(f"An error occurred during data entry process. {e}")
    finally:
        driver.quit()
        logger.info("WebDriver has been closed.")
