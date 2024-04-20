import json
from app.api.commons.captcha_solver import solveRecaptcha
from app.api.commons.gmail_fetch import fetch_facebook_codes, fetch_instagram_codes
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

def create_facebook_account(
    email,
    your_first_name,
    your_surname_name,
    your_password,
    birthday
):
    account_error = 0
    NotisCaptcha=False
    try:
        proxies = [
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "bzr6cmu2v9ntzmnhj3cqgb4",
        "password": "RNW78Fm5",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "gkecpblq8awl4s78gbr94ea",
        "password": "RNW78Fm5",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "dp3thm17jcn0t2blwz1lz2s",
        "password": "RNW78Fm5",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "8wmdx3xcr8raxfkpr6wr3o4",
        "password": "RNW78Fm5",
    },
    {
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "5st60xaow4vycmy93pnhasw",
        "password": "RNW78Fm5",
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

        "ip": "23.109.113.236",
        "port": 9000,
        "country": "USA",
        "countryCode": "US",
        "userName": "HjQDRTvBF9geWmQb",
        "password": "wifi;;;;",
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
        "ip": "185.130.105.109",
        "port": 10000,
        "country": "USA",
        "countryCode": "US",
        "userName": "i48gs3kt71c4hkv0mgqvz3p",
        "password": "RNW78Fm5",
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
    # {
    #     "ip": "185.130.105.109",
    #     "port": 10000,
    #     "country": "Canada",
    #     "countryCode": "CA",
    #     "userName": "7kbybxyykcakhpstr8r4b9v",
    #     "password": "RNW78Fm5",
    # },
        ]

        # Choose a random proxy from the list
        # proxy = random.choice(proxies)
        proxy=random_proxy()

        # proxy=proxies[9]
        proxy_string = f"{proxy['ip']}:{proxy['port']}"

        userName = proxy["userName"]
        password = proxy["password"]
        ip = proxy["ip"]
        port = proxy["port"]
        port=10694
        user_agent = UserAgent(browsers=['chrome'],min_percentage=2.1,os='windows')
        chrome_options = Options()
        # Set up proxy with authentication
        auth_options = {
            "proxy": {
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "https": f"https://{userName}:{password}@{ip}:{port}",
                # "no_proxy": "localhost,127.0.0.1",
            }
        }

        # Configure Chrome options for headless mode and to prevent detection
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
            "https://www.facebook.com/reg/"
        )
        wait = WebDriverWait(driver, 10)
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
                driver.find_element(By.NAME, "reg_email__").send_keys(phone_number['number'])

                break
        except Exception as e:
            pass
        driver.find_element(By.NAME, "firstname").send_keys(your_first_name)
        driver.find_element(By.NAME, "lastname").send_keys(your_surname_name)
        # driver.find_element(By.NAME, "reg_email__").send_keys(email)
        # driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(email)

        driver.find_element(By.ID, "password_step_input").send_keys(your_password)
        month_dropdown = Select(driver.find_element(By.ID, "month"))
        select_day = Select(wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@title='Day']"))))
        select_year = Select(wait.until(EC.element_to_be_clickable((By.NAME, "birthday_year"))))

        birthday_elements = birthday.split()

        select_day.select_by_visible_text(birthday_elements[0])
        month_dropdown.select_by_value(birthday_elements[1])
        select_year.select_by_visible_text(birthday_elements[2])
        driver.find_element(By.XPATH, "//label[text()='Male']").click()

        driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()

        driver.implicitly_wait(30)
        try:
            driver.switch_to.default_content()

            continue_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Continue'][role='button']")

            # Click the "Continue" button
            continue_button.click()
        except:
            pass

        try:
            time.sleep(10)
            sms=get_sms_v2(phone_number['request_id'])
            time.sleep(5)  # Adjust the sleep time according to your page's load time

            # Find the input field by its ID and input your code
            input_field = driver.find_element(By.ID, 'code_in_cliff')
            input_field.send_keys(sms['sms_code'])     
        except Exception as e:
            pass
        try:
            
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "u_9_3_ho")))

            # Click the button by ID
            button = driver.find_element(By.ID, "u_9_3_ho")
            button.click()
        except Exception as e:
            print("Continue button not found.")
            pass
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "confirm")))

            button = driver.find_element(By.NAME, "confirm")
            button.click()
        except Exception as e:
            pass
        try:
            # Wait for the popup modal to be visible
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "._42ft._42fu.layerCancel.uiOverlayButton.selected._42g-._42gy")))

            # Click the button
            button = driver.find_element(By.CSS_SELECTOR, "._42ft._42fu.layerCancel.uiOverlayButton.selected._42g-._42gy")
            button.click()
            NotisCaptcha=True

        except:
            pass
        # try:
        #     time.sleep(10)
        #     sms=get_sms_v2(phone_number['request_id'])
        #     input_field = driver.find_element(By.ID, ":r3:")
        #     input_field.send_keys(code)
        # except Exception as e:
        #     pass
        if NotisCaptcha is False:
        
            try:
            # Use WebDriverWait to wait for the iframe to be present
            # WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'www.google.com/recaptcha/api2/anchor')]"))
            # )
            # iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'www.google.com/recaptcha/api2/anchor')]")

            # # Extract the URL from the src attribute of the iframe
            # site_url = iframe.get_attribute('src')

            # # Store the URL in a variable
            # print("Site URL: ", site_url)
                try:
                # Wait for the outer iframe to be present and switch to it
                # outer_iframe = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.ID, "captcha-recaptcha"))
                # )
                # driver.switch_to.frame(outer_iframe)

                # WebDriverWait(driver, 10).until(
                # EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))
                # )
                # inner_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                # driver.switch_to.frame(inner_iframe)
                    WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, "captcha-recaptcha"))
                    )

                    # Find the inner iframe and get its 'src' attribute without switching to it
                    inner_iframe_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]'))
                    )
                    iframe_src = inner_iframe_element.get_attribute('src')
                    print("URL of the iframe: ", iframe_src)
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
                try:
                    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
                    recaptcha_response_textarea = driver.find_element(By.ID, "g-recaptcha-response")
                    recaptcha_response_textarea.send_keys(code)
                except:
                    pass
            except Exception as e:
                pass
            try:
            # After setting the g-recaptcha-response value
            #token = 'your_captcha_token_here'  # Replace with your actual token
                driver.execute_script("successCallback(arguments[0])", code)
            except Exception as e:
                pass
        
            try:
                # Wait for the element to be present before attempting to click
                # Replace WebDriverWait and expected_conditions as needed for dynamic pages
                # Find the "Continue" button using its attributes and click it
                continue_button = driver.find_element(By.XPATH, "//div[@aria-label='Continue']")
                continue_button.click()
                print("Continue button not found")
            except Exception as e:
                print("Continue button not found.")
                pass
            try:
                email_input = driver.find_element(By.XPATH, "//label[@aria-label='Enter email address']//input")
                email_input.send_keys(email)
            except Exception as e:
                pass
            try:
                wait = WebDriverWait(driver, 10)
                send_login_code_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Send Login Code'][@role='button']")))

                # Click the "Send Login Code" button
                send_login_code_button.click()
            except Exception as e:
                pass
            try:
            # Locate the input field by its id and enter the 5-digit code
                otp_all = fetch_facebook_codes(email, 'cvud vbwq otdo zwrf')
                input_field = driver.find_element(By.ID, ":r3:")
                input_field.send_keys(code)
            except Exception as e:
                pass
            try:
                otp_all = fetch_facebook_codes(email, 'cvud vbwq otdo zwrf')
                otp_codes=otp_all['facebook_codes']
                size=len(otp_codes)
                otp=otp_codes[size-1]
                for retry in range(5):
                    if len(otp_all["facebook_codes"]) == 0:
                        otp_all = fetch_facebook_codes(email, 'rlyc iujl fwqn ajaa')
                        continue
                    otp_codes=otp_all['facebook_codes']
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
            except Exception as e:
                pass
            try:
                next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next'][@role='button']"))
                )
                next_button.click()
            except Exception as e:
                pass
        
            print("next")
        driver.quit()
        print("account created successfully")
        return "Account created successfully"
    except Exception as e:
        pass


def create_facebook_account_phone(
    email,
    your_first_name,
    your_surname_name,
    your_password,
    birthday
):
    account_error = 0
    try:
        proxies = [
    
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
        proxy = random.choice(proxies)
        proxy=proxies[0]

        # proxy = random_proxy()
        proxy_string = f"{proxy['ip']}:{proxy['port']}"

        userName = proxy["userName"]
        password = proxy["password"]
        ip = proxy["ip"]
        port = proxy["port"]
        user_agent = UserAgent(browsers=['chrome'],min_percentage=2.1,os='windows')
        chrome_options = Options()
        # Set up proxy with authentication
        auth_options = {
            "proxy": {
                "http": f"http://{userName}:{password}@{ip}:{port}",
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
        random_user_agent = user_agent.random
        chrome_options.add_argument(f'user-agent={random_user_agent}')
        driver = webdriver.Chrome(
            options=chrome_options,
            seleniumwire_options=auth_options
        )  # Initialize your WebDriver here with the appropriate path
        # driver = webdriver.Firefox()  # Initialize your WebDriver here with the appropriate path
        driver.get(
            "https://www.facebook.com/reg/"
        )
        wait = WebDriverWait(driver, 10)
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
                driver.find_element(By.NAME, "reg_email__").send_keys(phone_number['number'])

                break
        except Exception as e:
            pass
        driver.find_element(By.NAME, "firstname").send_keys(your_first_name)
        driver.find_element(By.NAME, "lastname").send_keys(your_surname_name)
        driver.find_element(By.ID, "password_step_input").send_keys(your_password)
        month_dropdown = Select(driver.find_element(By.ID, "month"))
        select_day = Select(wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@title='Day']"))))
        select_year = Select(wait.until(EC.element_to_be_clickable((By.NAME, "birthday_year"))))

        birthday_elements = birthday.split()

        select_day.select_by_visible_text(birthday_elements[0])
        month_dropdown.select_by_value(birthday_elements[1])
        select_year.select_by_visible_text(birthday_elements[2])
        driver.find_element(By.XPATH, "//label[text()='Male']").click()

        driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()

        driver.implicitly_wait(30)
        try:
            continue_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Continue'][role='button']")

            # Click the "Continue" button
            continue_button.click()
        except:
            pass
        try:
            # Use WebDriverWait to wait for the iframe to be present
            # WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'www.google.com/recaptcha/api2/anchor')]"))
            # )
            # iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'www.google.com/recaptcha/api2/anchor')]")

            # # Extract the URL from the src attribute of the iframe
            # site_url = iframe.get_attribute('src')

            # # Store the URL in a variable
            # print("Site URL: ", site_url)
            try:
                # Wait for the outer iframe to be present and switch to it
                # outer_iframe = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.ID, "captcha-recaptcha"))
                # )
                # driver.switch_to.frame(outer_iframe)

                # WebDriverWait(driver, 10).until(
                # EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]'))
                # )
                # inner_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                # driver.switch_to.frame(inner_iframe)
                WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "captcha-recaptcha"))
                )

                # Find the inner iframe and get its 'src' attribute without switching to it
                inner_iframe_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]'))
                )
                iframe_src = inner_iframe_element.get_attribute('src')
                print("URL of the iframe: ", iframe_src)
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
            try:
                driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
                recaptcha_response_textarea = driver.find_element(By.ID, "g-recaptcha-response")
                recaptcha_response_textarea.send_keys(code)
            except:
                pass
        except Exception as e:
            pass
        try:
            # After setting the g-recaptcha-response value
            #token = 'your_captcha_token_here'  # Replace with your actual token
            driver.execute_script("successCallback(arguments[0])", code)
        except Exception as e:
            pass
        
        try:
            
            continue_button = driver.find_element(By.XPATH, "//div[@aria-label='Continue']")
            continue_button.click()
            print("Continue button not found")
        except Exception as e:
            print("Continue button not found.")
            pass
        try:
            time.sleep(10)
            sms=get_sms_v2(phone_number['request_id'])
            time.sleep(5)  # Adjust the sleep time according to your page's load time

            # Find the input field by its ID and input your code
            input_field = driver.find_element(By.ID, 'code_in_cliff')
            input_field.send_keys(sms['sms_code'])     
        except Exception as e:
            pass
        try:
            button = driver.find_element(By.ID, 'u_9_3_ns')
            button.click()
        except Exception as e:
            pass
        try:
            
            # Find the input field for the OTP and enter the OTP code
            otp_input_field = driver.find_element(By.CSS_SELECTOR, "input[name='email_confirmation_code']")
            otp_input_field.clear()  # Clear the field in case there's any pre-filled value
            otp_input_field.send_keys(sms['sms_code'])
            time.sleep(5)
                # Find the "Next" button and click it
            next_button = driver.find_element(By.XPATH, "//div[@role='button'][contains(text(),'Next')]")
            next_button.click()
            time.sleep(10)
        except Exception as e:
            pass
        try:
            next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next'][@role='button']"))
            )
            next_button.click()
        except Exception as e:
            pass
        
        print("next")
    except Exception as e:
        pass