import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sendgrid_helper




def _login():
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_SHIM')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get("https://stackoverflow.com")

        driver.find_element_by_link_text("Log In").click()

        driver.find_element_by_id("email").send_keys(os.environ['STACK_OVERFLOW_EMAIL'])
        driver.find_element_by_id("password").send_keys(os.environ['STACK_OVERFLOW_PASSWORD'])
        driver.find_element_by_id("submit-button").submit()

        driver.find_element_by_class_name("my-profile").click()

        elem = driver.find_element_by_class_name("mini-avatar")
        assert os.environ['STACK_OVERFLOW_DISPLAY_NAME'] in elem.text
        print("Logged into stackoverflow.com and accessed profile page")

    except Exception as e:
        message = "An error occurred while trying to access stackoverflow.com!"
        print(message, e)
        raise

    finally:
        driver.close()




def login():
    print("Logging into stackoverflow.com")
    last_exception = None

    for i in range(1000):
        try:
            _login()
            break
        except Exception as e:
            last_exception = e
            time.sleep(1)
    else:
        sendgrid_helper.send_mail("Login FAILED alert!", "Tried 1000 times to login, but it did not work")
        message = "ERROR after 1000 attempts"
        print(message, last_exception)




if __name__ == "__main__":
    login()
