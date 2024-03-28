import json
from app.api.commons.gmail_fetch import fetch_instagram_codes
from app.api.commons.sms_provider import (
    find_country_by_name,
    get_activation,
    get_all_countries_v2,
    get_countries,
    get_countries_v2,
    get_numbers_v2,
    get_phone_number,
    get_phone_number_vpa,
    get_sms_activation,
    get_sms_v2,
)

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
import time
from selenium.webdriver.common.action_chains import ActionChains

def create_insta_account(
    email,
    your_full_name,
    your_username,
    your_password,
    birthday,
    app_password
):
    account_error = 0
    try:
        proxies = [
    {
        "ip": "geo.iproyal.com",
        "port": 12321,
        "country": "USA",
        "countryCode": "US",
        "userName": "s0I6x7P090XXBD40",
        "password": "9AhOmAaN08U00XKY_country-us",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "k1rfffj5htpldoy4xols8zl",
        "password": "RNW78Fm5",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "mzlszp1mv95hxqgeo1302vf",
        "password": "RNW78Fm5",
    },
        ]

        # Choose a random proxy from the list
        proxy = random.choice(proxies)
        #proxy=proxies[0]
        proxy_string = f"{proxy['ip']}:{proxy['port']}"

        userName = proxy["userName"]
        password = proxy["password"]
        ip = proxy["ip"]
        port = proxy["port"]
        # Set up proxy with authentication
        auth_options = {
            "proxy": {
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "no_proxy": "localhost,127.0.0.1",
            }
        }

        # Configure Chrome options for headless mode and to prevent detection
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument(f'--proxy-server={proxy_string}')

        # # Add additional arguments to prevent detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=auth_options
        )  # Initialize your WebDriver here with the appropriate path
        # driver = webdriver.Firefox()  # Initialize your WebDriver here with the appropriate path
        driver.get(
            "https://www.instagram.com/accounts/emailsignup/"
        )
        wait = WebDriverWait(driver, 10)

        # Fill in the form
        email_or_phone = wait.until(EC.visibility_of_element_located((By.NAME, "emailOrPhone")))
        email_or_phone.send_keys(email)

        full_name = driver.find_element(By.NAME, "fullName")
        full_name.send_keys(your_full_name)

        username = driver.find_element(By.NAME, "username")
        username.send_keys(your_username)

        password = driver.find_element(By.NAME,  "password")
        password.send_keys(your_password)

        # Click the Sign Up button
        # Since the button is disabled by default, ensure all fields are correctly filled to enable it.
        time.sleep(5)
        sign_up_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        sign_up_button.click()
        time.sleep(5)

        # Selecting the dropdowns for month, day, and year by their title attributes
        select_month = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Month:']"))))
        select_day = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Day:']"))))
        select_year = Select(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "select[title='Year:']"))))

        birthday_elements = birthday.split()
        # Replace these values with the actual birthdate
        select_month.select_by_value(birthday_elements[1])  # January
        select_day.select_by_value(birthday_elements[0])    # 1st
        select_year.select_by_value(birthday_elements[2])  # 1990
        time.sleep(5)

        try:
        # Clicking the "Next" button
            wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._acan._acap._acaq._acas._aj1-._ap30')))
            next_button.click()
        except:
            pass
        try:
            time.sleep(10)
            otp_all = fetch_instagram_codes(email, app_password)
            for retry in range(5):
                if len(otp_all["instagram_codes"]) == 0:
                    otp_all = fetch_instagram_codes(email, app_password)
                    continue
                otp_codes=otp_all['instagram_codes']
                size=len(otp_codes)
                otp=otp_codes[size-1]
                # Find the input field for the OTP and enter the OTP code
                otp_input_field = driver.find_element(By.CSS_SELECTOR, "input[name='email_confirmation_code']")
                otp_input_field.clear()  # Clear the field in case there's any pre-filled value
                otp_input_field.send_keys(otp)
                time.sleep(5)

                    # Find the "Next" button and click it
            
                next_button = driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'Next')]")
                next_button.click()
                time.sleep(10)
                try:
                    error_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), \"That code isn't valid. You can request a new one.\")]"))
                    )

                # If the error message is present, find and click the "Resend code" button
                    if error_message:
                        resend_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Resend code.')]")
                        resend_button.click()
                        print("Resend code button clicked due to error.")
                        otp_all = fetch_instagram_codes(email, app_password)
                        continue
                    break
                except Exception as e:
                    print("Either there was no error, or the 'Resend code' button was not found.", e)


            

    # Optionally, add any follow-up actions after clicking "Next"
            print(f"An error occurred: ")

        except Exception as e:
            print(f"An error occurred: {e}")
    except Exception as e:
        pass
        