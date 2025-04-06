#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as Options_Chrome
from selenium.webdriver.chrome.service import Service  # Import Service for ChromeDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime  # Added for logging time
from time import sleep

# User data directly integrated
user_data = {
    "ip": "192.168.68.1",
    "password": "TPlinkAbsolon123",
    "browser": "Chrome",
    "browser_display": "yes",
    "execute_reboot": "yes",
    "text_reboot": "Reboot",
    "text_reboot_all": "REBOOT ALL",
    "text_model": "X50-DSL"
}

# Browser setup for Chrome
chrome_options = Options_Chrome()
if user_data["browser_display"].lower() != "yes":
    chrome_options.add_argument("--headless")  # Enable headless mode if browser display is disabled
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  # Helps with limited resource environments

# Specify the path to ChromeDriver using Service
chrome_service = Service('/usr/bin/chromedriver')

# Create the WebDriver instance using Service
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Maximize the Chrome browser window
driver.maximize_window()

try:
    url = f"http://{user_data['ip']}"
    wait = WebDriverWait(driver, 10)

    # Open browser and login
    driver.get(url)
    wait.until(ec.visibility_of_element_located((By.ID, "local-login-pwd")))
    driver.find_element(By.CSS_SELECTOR, 'input.text-text:nth-child(1)').send_keys(user_data['password'])
    sleep(2)
    driver.find_element(By.LINK_TEXT, "LOG IN").click()

    # Navigate to the reboot page
    wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "folder-tree-folder-node-text")))
    driver.get(f'{url}/webpages/index.html#reboot')
    wait.until(ec.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'content') and text()='{user_data['text_model']}']")))

    # Prepare and execute reboot
    driver.find_element(By.LINK_TEXT, f"{user_data['text_reboot_all']}").click()
    wait.until(ec.visibility_of_element_located((By.XPATH, f"//span[contains(@class, 'text button-text') and text()='{user_data['text_reboot']}']")))
    sleep(20)
    if user_data['execute_reboot'].lower() == "yes":
        driver.find_element(By.XPATH, f"//span[contains(@class, 'text button-text') and text()='{user_data['text_reboot']}']").click()
        sleep(30)

        # Log successful execution with timestamp
        with open("deco.log", "a") as log_file:
            log_file.write(f"Script executed successfully at: {datetime.now()}\n")
    else:
        print("Reboot not executed. 'execute_reboot' set to 'no'.")
except Exception as e:
    # Log errors if any occur
    with open("deco.log", "a") as log_file:
        log_file.write(f"An error occurred at {datetime.now()}: {e}\n")
    print(f"An error occurred: {e}")
finally:
    driver.quit()
