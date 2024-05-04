import json
from typing import Optional

from httpcore import TimeoutException
from app.api.commons.proxies_list import random_proxy
from app.api.commons.sms_provider import (
    find_country_by_name,
    get_activation,
    get_all_countries_v2,
    get_code,
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
from urllib.parse import quote
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
proxy_error_loading_page=0
account_error = 0

def create_gmail_account(
    
    your_first_name,
    your_last_name,
    your_username,
    your_birthday,
    your_gender,
    your_password,
):
    global proxy_error_loading_page

    try:
        proxies = [
   
    {
        "ip": "103.214.44.131",
        "port": 12321,
        "country": "USA",
        "countryCode": "US",
        "userName": "s0I6x7P090XXBD40",
        "password": "9AhOmAaN08U00XKY_country-us",
    },
    
    {
        "ip": "167.235.26.46",
        "port": 11200,
        "country": "USA",
        "countryCode": "US",
        "userName": "s0I6x7P090XXBD40",
        "password": "9AhOmAaN08U00XKY_country-us_state-california",
    },
    # {
    #     "ip": "91.239.130.17",
    #     "port": 44443,
    #     "country": "USA",
    #     "countryCode": "US",
    #     "userName": "mr33386VXjx",
    #     "password": "MD0tmnCaTm_country-us_session-stgkc31k_lifetime-5m",
    # },
    # {
    #     "ip": "185.130.105.109",
    #     "port": 10000,
    #     "country": "USA",
    #     "countryCode": "US",
    #     "userName": "p56svt44x2eft0d9z4vfjw3",
    #     "password": "RNW78Fm5",
    # },
    # {
    #     "ip": "185.130.105.109",
    #     "port": 10000,
    #     "country": "USA",
    #     "countryCode": "US",
    #     "userName": "4zouumuibd2fpeo7c6vltbw",
    #     "password": "RNW78Fm5",
    # },
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
        "ip": "us.smartproxy.com",
        "port": 10001,
        "country": "USA",
        "countryCode": "US",
        "userName": "sprska2hoe",
        "password": "0Iy6oxisu0=LRN5bal",
    },
        ]
        # URL-encode username and password
        

        

        # Choose a random proxy from the list
        # proxy=random_proxy()

        # proxy = random.choice(proxies)
        proxy=proxies[5]
        proxy_string = f"{proxy['ip']}:{proxy['port']}"
        #10650
        userName = proxy["userName"]
        password = proxy["password"]
        ip = proxy["ip"]
        port = proxy["port"]
        # userName = quote(userName, safe='')
        # password = quote(password, safe='')
        # Set up proxy with authentication
        auth_options = {
            "proxy": {
                "http": f"http://{userName}:{password}@{ip}:{port}",
                "https": f"https://{userName}:{password}@{ip}:{port}",
                "no_proxy": "*.soax.com, localhost, 127.0.0.1,*.froxy.com,*smartproxy.com",
            }
        }

        # Configure Chrome options for headless mode and to prevent detection
        user_agent = UserAgent(browsers=['chrome'])
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument(f'--proxy-server={proxy_string}')
        
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

        try:
            driver.get(
            "https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp"
            )
        except Exception as e:
            if 'unknown error: net::ERR_TUNNEL_CONNECTION_FAILED' in e.msg and proxy_error_loading_page<5:
                proxy_error_loading_page+=1
                driver.quit()
                create_gmail_account(
                    your_first_name,
                    your_last_name,
                    your_username,
                    your_birthday,
                    your_gender,
                    your_password,
                )
            else:

                print("Can't open chrome due to invalid proxy")
                print(proxy)
                print(e)
                return None



        first_name = driver.find_element(By.NAME, "firstName")
        last_name = driver.find_element(By.NAME, "lastName")

        first_name.clear()
        first_name.send_keys(your_first_name)

        last_name.clear()
        last_name.send_keys(your_last_name)

        # Introduce random delay before clicking the "Next" button
        # time.sleep(random.uniform(1, 3))

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button/span[contains(text(), 'Next')]")
            )
        )
        next_button.click()

        # Introduce random delay before interacting with the birthday fields
        # time.sleep(random.uniform(1, 3))

        wait = WebDriverWait(driver, 20)
        day = wait.until(EC.visibility_of_element_located((By.NAME, "day")))

        birthday_elements = your_birthday.split()
        month_value = birthday_elements[1].lstrip('0')
        day_value=birthday_elements[0].lstrip('0')
        month_dropdown = Select(driver.find_element(By.ID, "month"))
        month_dropdown.select_by_value(month_value)

        day_field = driver.find_element(By.ID, "day")
        day_field.clear()
        day_field.send_keys(day_value)

        year_field = driver.find_element(By.ID, "year")
        year_field.clear()
        year_field.send_keys(birthday_elements[2])

        gender_dropdown = Select(driver.find_element(By.ID, "gender"))
        gender_dropdown.select_by_value(your_gender)

        # Introduce random delay before clicking the "Next" button
        # time.sleep(random.uniform(1, 3))

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button/span[contains(text(), 'Next')]")
            )
        )
        next_button.click()

        # Introduce random delay before interacting with the username field
        time.sleep(random.uniform(1, 3))

        try:
            create_own_option = wait.until(
                EC.element_to_be_clickable((By.ID, "selectionc4"))
            )
            create_own_option.click()
        except Exception as e:
            pass

        try:
            create_own_email = wait.until(
                EC.element_to_be_clickable((By.NAME, "Username"))
            )
        except Exception as e:
            print(e)
            pass

        username_field = driver.find_element(By.NAME, "Username")
        username_field.clear()
        username_field.send_keys(your_username)

        # Introduce random delay before clicking the "Next" button
        # time.sleep(random.uniform(1, 3))

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button/span[contains(text(), 'Next')]")
            )
        )
        next_button.click()

        # Introduce random delay before interacting with the password fields
        time.sleep(random.uniform(1, 3))

        password_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "Passwd"))
        )
        password_field.clear()
        password_field.send_keys(your_password)

        password_confirmation_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "PasswdAgain"))
        )
        password_confirmation_field.clear()
        password_confirmation_field.send_keys(your_password)

        # Introduce random delay before clicking the "Next" button
        # time.sleep(random.uniform(1, 3))

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button/span[contains(text(), 'Next')]")
            )
        )
        next_button.click()
        time.sleep(5)

        try:
            error_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(text(), 'Sorry, we could not create your Google Account')]",
                    )
                )
            )
            global account_error
            if (
                error_message.text == "Sorry, we could not create your Google Account."
                and account_error <= 5
            ):
                
                account_error = account_error + 1
                driver.quit()
                create_gmail_account(
                    your_first_name,
                    your_last_name,
                    your_username,
                    your_birthday,
                    your_gender,
                    your_password,
                )

        except Exception as e:
            # Check if the error message is present
            pass
        # Skip adding a phone number
        phone_number=0
        sms=0
        try:
            # Find the phone number input field and enter the phone number
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
            retry_count = 5
            for _ in range(retry_count):
                # country = get_countries()
                # countryId = find_country_by_name(country, 'Pakistan')
                # countryCode = proxy["countryCode"]
                # phone_number = get_phone_number(countryId["id"])
                # phone_input = driver.find_element(By.ID, "phoneNumberId")
                # phone_input.clear()
                # phone_input.send_keys(phone_number[0])

                # activationId = phone_number[1]
                country=187
                phone_number=get_phone_number(country)
                try:
                    if  phone_number ==None:
                        retry_count_1=5
                        for _ in range(retry_count_1):
                            name=proxy['country']
                            country=get_countries_v2(name)
                            phone_number=get_numbers_v2(country,122)
                            try:
                                if phone_number['error_code'] =="no_numbers":
                                    continue
                            except:
                                pass
                            sms=get_sms_v2(phone_number['request_id'])
                            if sms =="":
                                continue
                            else:
                                break
                        
                except Exception as e: 
                    pass
                phone_input = driver.find_element(By.ID, "phoneNumberId")
                phone_input.clear()
                phone_input.send_keys("+",phone_number['number'])
                next_button = WebDriverWait(driver, 10).until(
                     EC.element_to_be_clickable(
                         (By.XPATH, "//button/span[contains(text(), 'Next')]")
                     )
                 )
                next_button.click()
                try:
                    error_message = driver.find_element(
                        By.XPATH, "//div[contains(@class, 'jPtpFe')]"
                    )
                    if error_message and error_message.is_displayed():
                        print("Error message displayed. Retrying...")
                        time.sleep(2)  # Add a delay before retrying
                        continue
                except:
                    pass
                try:
                    error_message = driver.find_element(
                        By.XPATH, "//div[contains(@class, 'Ekjuhf')]"
                    )
                    if error_message and error_message.is_displayed():
                        print("Error message displayed. Retrying...")
                        time.sleep(2)  # Add a delay before retrying
                        continue
                except:
                    pass

                
                # while True:
                    #sms = get_activation(activationId)
                # sms=get_sms_v2(phone_number['request_id'])
                sms=get_code(phone_number['activation'])
                if sms =="":
                    try:
                        # Wait for the button to be clickable
                        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Get new code"]')))
                        # Click the button
                        button.click()
                        # Optionally, close the driver after operation is complete
                        # driver.quit()
                    except Exception as e:
                        print("Error:", e)
                    # sms=get_sms_v2(phone_number['request_id'])
                    # if sms=="":
                    continue
                else:
                    break    
                    # if sms == "":
                    #     # phone_number = get_phone_number_vpa(proxy["countryCode"])
                    #     # orderId = json.loads(phone_number)
                    #     # orderId = orderId["data"]["orderId"]
                    #     # otpCode = get_sms_activation(orderId)
                    #     # phone_input = driver.find_element(By.ID, "phoneNumberId")
                    #     # phone_input.clear()
                    #     # if otpCode == "":
                    #     #     break
                    #     # sms= json.load(otpCode)
                    #     # sms = otpCode["data"]["sms"]["code"]
                    #     #break
                    #     sms=000000
                    #     break
                    # else:
                    #     sms_json = json.loads(sms)
                    #     if sms_json["statusCode"] == 200:
                    #         print("Received SMS with statusCode 200.")
                    #         # Extract smsCode
                    #         sms = sms_json["activeActivations"][0]["smsCode"][0]
                    #         break  # Break out of the loop since we received the SMS successfully
                    #     elif sms_json["statusCode"] == 202:
                    #         # If statusCode is 202, continue to fetch SMS
                    #         print("Received SMS with statusCode 202. Retrying...")
                    #         continue
                    #     else:
                    #         # If statusCode is neither 200 nor 202, handle the error
                    #         print(
                    #             "Received SMS with unexpected statusCode:",
                    #             sms_json["statusCode"],
                    #         )
                    #         break  # Break out of the loop to avoid infinite looping
                # next_button = WebDriverWait(driver, 10).until(
                #     EC.element_to_be_clickable(
                #         (By.XPATH, "//button/span[contains(text(), 'Next')]")
                #     )
                # )
                # next_button.click()
                # try:
                #     error_message = driver.find_element(
                #         By.XPATH, "//div[contains(@class, 'jPtpFe')]"
                #     )
                # except:
                #     pass
                # try:
                #     error_message = driver.find_element(
                #         By.XPATH, "//div[contains(@class, 'Ekjuhf')]"
                #     )
                # except:
                #     pass

                # if error_message and error_message.is_displayed():
                #     print("Error message displayed. Retrying...")
                #     time.sleep(2)  # Add a delay before retrying
                #     continue
            otp_input = (
                WebDriverWait(driver, 10)
                .until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="code"]'))
                )
                .send_keys(sms['sms_code'])
            )
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button/span[contains(text(), 'Next')]")
                )
            )
            next_button.click()
        except Exception as e:
            print(e)
            pass

        # try:
        #     # Skip add recovery email
        #     skip_button_is_visible = wait.until(
        #         EC.visibility_of_element_located(
        #             (By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")
        #         )
        #     )
        #     skip_button = driver.find_element(
        #         By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d"
        #     )
        #     skip_button.click()

        #     # next_button = WebDriverWait(driver, 10).until(
        #     #     EC.element_to_be_clickable(
        #     #         (By.XPATH, "//button/span[contains(text(), 'Next')]")
        #     #     )
        #     # )
        #     # next_button.click()
        # except Exception as e:
        #     print(e)
        #     pass
        # try:
        #     skip_button_is_visible = wait.until(
        #         EC.visibility_of_element_located(
        #             (By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")
        #         )
        #     )
        #     skip_button = driver.find_element(
        #         By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d"
        #     )
        #     skip_button.click()
        # except Exception as e:
        #     print(e)
        #     pass
        try:
            skip_button=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), 'Skip')]")
                )
            )
            # skip_button = driver.find_element(
            #     By.XPATH, "//span[contains(text(), 'Skip')]"
            # )
            skip_button.click()
        except:
            pass
        try:
            wait = WebDriverWait(driver, 20)
            skip_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))

            # Click the skip button
            skip_button.click()
        except:
            pass
        time.sleep(5)
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button/span[contains(text(), 'Next')]")
                )
            )
            next_button.click()
        except:
            pass
        try:
            wait = WebDriverWait(driver, 20)
            next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "VfPpkd-LgbsSe")))

            # Click the skip button
            next_button.click()
        except:
            pass
        try:
            # Wait for the options to be visible
            options = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.oJeWuf"))
            )

            # Choose the first option
            first_option = options[0]
            first_option.click()
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button/span[contains(text(), 'Next')]")
                )
            )
            next_button.click()
        except:
            pass
        try:

            #scroll a few pixels over here
            # Wait for the "Accept all" button to be clickable
            accept_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(), 'Accept all')]")
                )
            )

            # Click the "Accept all" button
            accept_all_button.click()

        except Exception as e:
            print("Error:", e)
        try:
            # Agree on Google's privacies
            agree_button = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")
                )
            )
            agree_button.click()
        except Exception as e:
            print(e)
            pass
        time.sleep(4)
        

        try:
            agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='I agree']"))
            )
            agree_button.click()
        except:
            pass
        # Introduce random delay before closing the browser
        time.sleep(random.uniform(1, 10))
        # Wait for the page to load and the security button to be clickable
#         try:
#             # Wait for the security button to be clickable
#             security_button_xpath = "//*[@id='yDmH0d']/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[1]/div[3]/c-wiz/nav/ul/li[4]/a"
#             security_button = wait.until(EC.element_to_be_clickable((By.XPATH, security_button_xpath)))
#             security_button.click()
#             print("Security button clicked successfully.")
#         except Exception as e:
#             pass

#         try:
#         # Wait for the "2-Step Verification" section to become clickable.
#             two_step_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "2-Step Verification")]'))
#             )

#             # Click the "2-Step Verification" button.
#             two_step_button.click()
#         except Exception as e:
#             pass

        
        
        
#         try:
#             # Wait for the "Get started" button to be clickable
#             get_started_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "//span[text()='Get started']"))
#             )

#             # Click the "Get started" button
#             get_started_button.click()
#             time.sleep(10)
#         except Exception as e:
#             pass

#         # try:
#         #         button=WebDriverWait(driver, 10).until(
#         #         EC.element_to_be_clickable((By.CSS_SELECTOR, "[jsname='V67aGc']")))
#         #         # button = driver.find_element(By.CSS_SELECTOR, "[jsname='V67aGc']")
#         #         button.click()
#         # except Exception as e:
#         #     pass
        


#         # try:
#         #     password_field = wait.until(
#         #     EC.visibility_of_element_located((By.NAME, "Passwd"))
#         #     )
#         #     password_field.clear()
#         #     password_field.send_keys(your_password)
#         #     next_button = WebDriverWait(driver, 10).until(
#         #     EC.element_to_be_clickable(
#         #     (By.XPATH, "//button/span[contains(text(), 'Next')]")
#         #     )
#         #     )
#         #     next_button.click()
#         #     time.sleep(5)
#         # except Exception as e:
#         #     pass
#         try:
#             # Find the phone number input field and enter the phone number
#             # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
#             retry_count = 5
#             for _ in range(retry_count):
#                 # country = get_countries()
#                 # countryId = find_country_by_name(country, 'Pakistan')
#                 # countryCode = proxy["countryCode"]
#                 # phone_number = get_phone_number(countryId["id"])
#                 # phone_input = driver.find_element(By.ID, "phoneNumberId")
#                 # phone_input.clear()
#                 # phone_input.send_keys(phone_number[0])

#                 # activationId = phone_number[1]
#                 name=proxy['country']
#                 country=get_countries_v2(name)
#                 phone_number=get_numbers_v2(country,122)
#                 try:
#                     if phone_number['error_code'] =="no_numbers":
#                         retry_count_1=5
#                         for _ in range(retry_count_1):
#                             country=get_all_countries_v2()
#                             phone_number=get_numbers_v2(country,122)
#                             try:
#                                 if phone_number['error_code'] =="no_numbers":
#                                     continue
#                             except:
#                                 pass
#                             sms=get_sms_v2(phone_number['request_id'])
#                             if sms =="":
#                                 continue
                    
                        
#                 except Exception as e: 
#                     pass
#                 try:
#                     input_field = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))
#                     )

#                     # Clear any existing value in the input field
#                     input_field.clear()

#                     # Enter the phone number
#                     input_field.send_keys(phone_number['number'])
#                 except Exception as e:
#                     pass
#                 # try:
                    
#                 #     # Find the phone number input element by its id or other attributes
#                 #     phone_input = driver.find_element(By.ID, 'c51')  # You'd replace 'c51' with the actual ID or other selector of the input

#                 #     # Send the phone number to the input
#                 #     phone_input.send_keys(phone_number)
#                 except :
#                     pass
        
        
                
#                 try:
#                     next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
#                     next_button.click()
#                 except Exception as e:
#                     pass
#                 # try:
#                 #     # This XPath looks for a <span> element with text "Next" inside a div with specific class attributes
#                 #     next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]/ancestor::div[contains(@class, 'U26fgb O0WRkf oG5Srb HQ8yf C0oVfc') and not(contains(@style, 'display: none'))]")
#                 #     next_button.click()
#                 #     print("Next button clicked successfully!")
#                 # except Exception as e:
#                 #     print("Error finding or clicking the Next button:", e)

#                 except: 
#                     pass
#                 try:
#                     error_message= driver.find_element(By.XPATH,"//div[contains(@class, 'dEOOab') and contains(@class, 'RxsGPe') and contains(text(), 'Invalid number, try again.')]")
#                     if error_message and error_message.is_displayed():
#                         print("Error message displayed. Retrying...")
#                         time.sleep(2)  # Add a delay before retrying
#                         continue
#                 except Exception as e:
#                     pass

#                 # while True:
#                     #sms = get_activation(activationId)
#                 sms=get_sms_v2(phone_number['request_id'])

#                 if sms =="":

#                     # sms=get_sms_v2(phone_number['request_id'])
#                     # if sms=="":
#                     continue
#                 else:
#                     break    
#         except Exception as e:
#             pass

        
#         try:
#         # Find the input field by its class name
#             input_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "whsOnd"))
#             )

#         # Clear any existing value in the input field
#             input_field.clear()

#         # Enter the code
#             code = sms  # Replace "YOUR_CODE_HERE" with the desired code
#             input_field.send_keys(code['sms_code'])
#             try:
#                 next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
#                 next_button.click()
#             except Exception as e:
#                 pass
#         except Exception as e:
#             pass
        

#         try:
#         # Find the "Turn on" button by its class name
#             turn_on_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'RveJvd snByac') and text()='Turn on']")))

#             # Click the "Turn on" button
#             turn_on_button.click()

#         except Exception as e:
#             pass
#         time.sleep(5)

#         try:
        
#             verification_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div:nth-child(2) > div > c-wiz > c-wiz > div > div.s7iwrf.gMPiLc.Kdcijb > div > div > c-wiz > section > div:nth-child(4) > div > div > div:nth-child(2)")))

#             # Click on the 2-Step Verification button
#             verification_button.click()

#         except Exception as e:
#             pass

#         time.sleep(5)

#         try:
#             # Scroll to the "App passwords" link
#             app_passwords_link = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'App passwords')]"))
#             )
#             driver.execute_script("arguments[0].scrollIntoView();", app_passwords_link)

#             # Use a CSS Selector to find the link by part of its href attribute and click it
#             app_passwords_link = driver.find_element(By.CSS_SELECTOR,"a[href*='myaccount.google.com/apppasswords']")
#             app_passwords_link.click()
#         except Exception as e:
#             pass

        
#     #     try:
#     # # Wait for the ">" button to be clickable
#     #         wait = WebDriverWait(driver, 10)
#     #         app_passwords_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".GzPZ0c .U26fgb.mUbCce.fKz7Od.UQO9ef.zC7z7b.M9Bg4d .DPvwYc")))
        
#     #         # Scroll to the element
#     #         driver.execute_script("arguments[0].scrollIntoView(true);", app_passwords_button)
            
#     #         # Wait a moment for scrolling to finish
#     #         wait.until(EC.visibility_of(app_passwords_button))
        
#     #         # Try clicking the button again
#     #         app_passwords_button.click()
#     #     except Exception as e:
#     #         # If after waiting the click is still not possible, try clicking via JavaScript
#     #         driver.execute_script("arguments[0].click();", app_passwords_button)
#         try:
#             # Find the input field by its ID
#             input_field = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.ID, "i5"))
#             )

#             # Clear any existing text in the input field
#             input_field.clear()

#             # Enter text into the input field
#             input_field.send_keys("Gmail")

#             # Press Enter key to submit the input (if needed)
#             input_field.send_keys(Keys.RETURN)
#         except Exception as e:
#             pass

#         try:
#             # Find the button by its class name
#             create_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CLASS_NAME, "AeBiU-vQzf8d"))
#             )

#             # Click the button
#             create_button.click()
#         except Exception as e:
#             pass

#         try:
#             # Find the parent element containing the span elements
#             parent_element = driver.find_element(By.CSS_SELECTOR,'.bwApif-cnG4Wd')

#             # Find all span elements within the parent element
#             span_elements = parent_element.find_elements(By.CSS_SELECTOR,'span.v2CTKd.KaSAf')

# #            Extract the text content from each span element
#             text_contents = [span.text for span in span_elements]
#         except Exception as e:
#             pass

#         try:
#             # Wait for the password element to be loaded
#             password_element = WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, 'strong.v2CTKd'))
#             )
#             time.sleep(3)
#             # Extract the text from the element
#             app_password = password_element.text
#             print(app_password)
#         except:
#             pass
#         try:
#             done_button = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, "//span[text()='Done']"))
#             )

#             # Click the 'Done' button
#             done_button.click()
#         except:
#             pass
        # Close the browser window at the end of your automation
        driver.quit()

        print(
            "Your Gmail account has been successfully created:\nGmail: "
            + your_username
            + "@gmail.com\nPassword: "
            + your_password
        )
        account_error=6
        return {"username":your_username}
    except Exception as e:
        # Close the browser window in case of failure
        driver.quit()
        print("Failed to create your Gmail account. Please try again later.")
        print(e)
        return None

