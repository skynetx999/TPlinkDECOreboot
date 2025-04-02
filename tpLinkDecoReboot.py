from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as Options_Chrome
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

# User data directly integrated
user_data = {
    "log_level": "INFO",
    "ip": "192.168.68.1",
    "password": "TPlinkAbsolon123",
    "browser": "Chrome",
    "browser_display": "yes",
    "execute_reboot": "yes",
    "text_reboot": "Reboot",
    "text_reboot_all": "REBOOT ALL",
    "text_model": "X50-DSL",
    "mqtt_use": "yes",
    "mqtt_ip": "192.168.68.85",
    "mqtt_port": 1883,
    "mqtt_topic": "default_topic"
}

# Browser setup for Chrome
chrome_options = Options_Chrome()
if user_data["browser_display"].lower() != "yes":
    chrome_options.add_argument("--headless")  # Enable headless mode if browser display is disabled
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  # Helps with limited resource environments
driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')


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
    else:
        print("Reboot not executed. 'execute_reboot' set to 'no'.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
