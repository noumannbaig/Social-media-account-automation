import json
from app.api.commons.captcha_solver import solveRecaptcha
from app.api.commons.gmail_fetch import fetch_instagram_codes
from app.api.commons.proxies_list import random_proxy
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
from urllib.parse import quote

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
from fake_useragent import UserAgent

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
        "ip": "144.76.231.240",
        "port": 10002,
        "country": "USA",
        "countryCode": "US",
        "userName": "sprska2hoe",
        "password": "0Iy6oxisu0=LRN5bal",
    },
    {
        "ip": "167.235.26.46",
        "port": 11200,
        "country": "USA",
        "countryCode": "US",
        "userName": "s0I6x7P090XXBD40",
        "password": "9AhOmAaN08U00XKY_country-us_state-california",
    },
    {
        "ip": "91.239.130.17",
        "port": 44443,
        "country": "USA",
        "countryCode": "US",
        "userName": "mr33386VXjx",
        "password": "MD0tmnCaTm_country-us_session-stgkc31k_lifetime-5m",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "4zouumuibd2fpeo7c6vltbw",
        "password": "RNW78Fm5",
    },
    {
        "ip": "91.239.130.17",
        "port": 44443,
        "country": "USA",
        "countryCode": "US",
        "userName": "mr33386VXjx",
        "password": "MD0tmnCaTm_country-us_session-stgkc31k_lifetime-5m",
    },
    {
        "ip": "51.159.149.67",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "geonode_RCKrPAocFN",
        "password": "bc101ce5-1198-4176-af3e-dbc17510554e",
    },
    {
        "ip": "23.109.113.236",
        "port": 9000,
        "country": "USA",
        "countryCode": "US",
        "userName": "8ZiIPeu5FvocK47s",
        "password": "wifi;us;;;",
    },
    {
        "ip": "23.109.113.236",
        "port": 9000,
        "country": "USA",
        "countryCode": "US",
        "userName": "HjQDRTvBF9geWmQb",
        "password": "wifi;us;;;",
    },
    {
        "ip": "23.109.113.236",
        "port": 9000,
        "country": "USA",
        "countryCode": "US",
        "userName": "beSmgchc3wREs1dp",
        "password": "mobile;us;;;",
    },
    {
        "ip": "us.smartproxy.com",
        "port": 10001,
        "country": "USA",
        "countryCode": "US",
        "userName": "sprska2hoe",
        "password": "0Iy6oxisu0=LRN5bal",
    },
     {
        "ip": "185.162.130.82",
        "port": 10497,
        "country": "USA",
        "countryCode": "US",
        "userName": "RjYKZS1rCJbIcxfoy9TD_city_New-York",
        "password": "RNW78Fm5",
    },
        ]

        # Choose a random proxy from the list
        proxy = proxies[12]
        #proxy=random_proxy()
        proxy_string = f"{proxy['ip']}:{proxy['port']}"

        userName = proxy["userName"]
        password = proxy["password"]
        ip = proxy["ip"]
        port = proxy["port"]
        # userName = quote(userName, safe='')
        # password = quote(password, safe='')
        # Set up proxy with authentication
        auth_options = {
            "proxy": {
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "no_proxy": "*.soax.com,localhost,127.0.0.1,*.froxy.com,*us.smartproxy.com",
            }
        }

        # Configure Chrome options for headless mode and to prevent detection
        user_agent = UserAgent(browsers=['safari', 'chrome'],min_percentage=2.1)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(f'--proxy-server={proxy_string}')

        # # Add additional arguments to prevent detection

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        random_user_agent = user_agent.random
        chrome_options.add_argument(f'user-agent={random_user_agent}')
        driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=auth_options
        )  # Initialize your WebDriver here with the appropriate path
        # driver = webdriver.Firefox()  # Initialize your WebDriver here with the appropriate path
        driver.get(
            "https://www.instagram.com/accounts/emailsignup/"
        )
        wait = WebDriverWait(driver, 15)
        phone_number=0
        sms=0
        try:
            
            retry_count = 5
            for _ in range(retry_count):
               
                name=proxy['country']
                country=get_countries_v2(name)
                phone_number=get_numbers_v2(country,5)
                try:
                    if phone_number['error_code'] =="no_numbers":
                        retry_count_1=5
                        for _ in range(retry_count_1):
                            country=get_all_countries_v2()
                            phone_number=get_numbers_v2(country,122)
                            try:
                                if phone_number['error_code'] =="no_numbers":
                                    continue
                            except:
                                pass
                            sms=get_sms_v2(phone_number['request_id'])
                            if sms =="":
                                continue
                        
                except Exception as e: 
                    pass
                email_or_phone = wait.until(EC.visibility_of_element_located((By.NAME, "emailOrPhone")))
                email_or_phone.send_keys(phone_number['number'])
                break
        except Exception as e:
            pass
        # Fill in the form
        # email_or_phone = wait.until(EC.visibility_of_element_located((By.NAME, "emailOrPhone")))
        # email_or_phone.send_keys(email)

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
        print("started")

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
            action = ActionChains(driver)
            action.move_to_element(next_button).click().perform()
            next_button.click()
        except:
            pass
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "captcha-recaptcha"))
                )

                # Find the inner iframe and get its 'src' attribute without switching to it
            inner_iframe_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]'))
            )
            iframe_src = inner_iframe_element.get_attribute('src')
            print("URL of the iframe: ", iframe_src)
                #driver.switch_to.frame(outer_iframe)
            try:
                    # Wait for the checkbox to be clickable
                checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
                )
    
                    # Click the checkbox
                checkbox.click()
            except Exception as e:
                pass
        except :
            pass
            result = solveRecaptcha(
                "6Lc9qjcUAAAAADTnJq5kJMjN9aD1lxpRLMnCS2TR",
                iframe_src
            )

            code = result['code']

            print(code)

            try:
                time.sleep(3)
                driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

                driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", code)
                driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
            # Locate the hidden textarea for the reCAPTCHA response and set its value to the token
            except Exception as e:
                pass
        # try:
        #     time.sleep(10)
        #     otp_all = fetch_instagram_codes(email, app_password)
        #     for retry in range(5):
        #         if len(otp_all["instagram_codes"]) == 0:
        #             otp_all = fetch_instagram_codes(email, app_password)
        #             continue
        #         otp_codes=otp_all['instagram_codes']
        #         size=len(otp_codes)
        #         otp=otp_codes[size-1]
        #         # Find the input field for the OTP and enter the OTP code
        #         otp_input_field = driver.find_element(By.CSS_SELECTOR, "input[name='email_confirmation_code']")
        #         otp_input_field.clear()  # Clear the field in case there's any pre-filled value
        #         otp_input_field.send_keys(otp)
        #         time.sleep(5)

        #             # Find the "Next" button and click it
            
        #         next_button = driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'Next')]")
        #         next_button.click()
        #         time.sleep(10)
        #         try:
        #             error_message = WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located((By.XPATH, "//span[contains(text(), \"That code isn't valid. You can request a new one.\")]"))
        #             )

        #         # If the error message is present, find and click the "Resend code" button
        #             if error_message:
        #                 resend_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Resend code.')]")
        #                 resend_button.click()
        #                 print("Resend code button clicked due to error.")
        #                 otp_all = fetch_instagram_codes(email, app_password)
        #                 continue
        #             break
        #         except Exception as e:
        #             print("Either there was no error, or the 'Resend code' button was not found.", e)

        try:
            time.sleep(10)
            sms=get_sms_v2(phone_number['request_id'])
            
                # Find the input field for the OTP and enter the OTP code
            # otp_input_field = driver.find_element(By.CSS_SELECTOR, "input[name='email_confirmation_code']")
            otp_input_field = driver.find_element(By.NAME, 'confirmationCode')
            otp_input_field.clear()  # Clear the field in case there's any pre-filled value
            otp_input_field.send_keys(sms['sms_code'])
            time.sleep(5)

                    # Find the "Next" button and click it
            
            next_button = driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'Confirm')]")
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
            except Exception as e:
                print("Either there was no error, or the 'Resend code' button was not found.", e)

            

    # Optionally, add any follow-up actions after clicking "Next"
            print(f"An error occurred: ")

        except Exception as e:
            print(f"An error occurred: {e}")
    except Exception as e:
        pass
        