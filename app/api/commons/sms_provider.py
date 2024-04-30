import http.client
import json
import random
import time

import requests


def get_phone_number_vpa(countryCode: str):
    conn = http.client.HTTPSConnection("api.smspva.com")
    headers = {"apikey": "75YzNW4JEeqq23CsxKOAYAXBILYUQ8"}
    conn.request("GET", f"/activation/number/{countryCode}/opt1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


import http.client


def get_sms_activation(orderId: int):
    count_status = 0
    code = ""
    # while(True):
    while count_status < 5:
        conn = http.client.HTTPSConnection("api.smspva.com")
        headers = {"apikey": "75YzNW4JEeqq23CsxKOAYAXBILYUQ8"}
        conn.request("GET", f"/activation/sms/{orderId}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        response = data.decode("utf-8")
        response=json.loads(response)
        if response["statusCode"] == 202:
            time.sleep(10)
            continue
        elif response["statusCode"] == 200:
            return response
        else:
            return ""


from smsactivate.api import SMSActivateAPI

# SMSActivateAPI Contains all basic tools for working with the SMSActivate API
sa = SMSActivateAPI("0e931580379e03b801fe03230Ae2021f")
sms_activate_url = "https://sms-activate.org/stubs/handler_api.php"
phone_request_params = {
    "api_key": "0e931580379e03b801fe03230Ae2021f",
    "action": "getNumber",
    "country": 47,
    "service": "go",
}

status_param = {"api_key": "0e931580379e03b801fe03230Ae2021f", "action": "getStatus"}


def get_phone_number(country: int):
    count = 0
    while count < 5:
        phone_request_params["country"] = country
        res = requests.get(url=sms_activate_url, params=phone_request_params)
        data = res.text
        print(data)
        if "ACCESS_NUMBER" in data:
            activationId = data.split(":")[1]
            number = data.split(":")[2]

            number = "+" + number
            print(number)
            return [number, activationId]

        if "NO_BALANCE" in data:
            print("Check your Balance in sms-activate.")
            return
        count = count + 1
        time.sleep(2)
        if number == "":
            print(
                "################ Cannot get phone number: ",
                5,
                " times retrial. ################",
            )
            return


def get_activation(activationId):
    count_status = 0
    code = ""
    # while(True):
    while count_status < 5:
        status_param["id"] = activationId
        print(status_param)
        res_code = requests.get(url=sms_activate_url, params=status_param)
        data_code = res_code.text
        print(data_code)
        if "STATUS_OK" in data_code:
            code = data_code.split(":")[1]
            return code
        count_status = count_status + 1
        time.sleep(15)
    if code == "":
        print("Cannot receive code from sms_activate: ", 5, " times retrial")
        return ""
def get_code(id: str):
    # Construct the API URL for checking the activation status
    url = f"https://api.sms-activate.org/stubs/handler_api.php?api_key=0e931580379e03b801fe03230Ae2021f&action=getStatus&id={id}"

    import time
    start_time = time.time()

    # Wait and poll for the verification code
    while time.time() - start_time < 180:
        response = requests.get(url)
        if response.status_code != 200:
            return ""

        response_content = response.text

        if response_content.startswith("STATUS_OK"):
            # Extract the code from the response
            code = response_content.split(":")[1]
            return code

        # Sleep for a short interval before checking again
        time.sleep(10)

    return ""

def get_countries():
    return sa.getCountries()

def get_countries_v2(countryName:str):
    token="mwCLHHjqs8f-M9bHZ6Bo8srAXCojX6Rn"
    target_url = f"https://api.sms-man.com/control/countries?token={token}"
    response = requests.get(target_url)
    countries= response.json()
    for country_id, country_info in countries.items():
        if country_info['title'] in countryName:
            return country_id
    return None

def get_all_countries_v2():
    token="mwCLHHjqs8f-M9bHZ6Bo8srAXCojX6Rn"
    target_url = f"https://api.sms-man.com/control/countries?token={token}"
    response = requests.get(target_url)
    countries= response.json()
    return random.choice(list(countries))

def find_country_by_name(country_data, country_name):
    for country_id, country_info in country_data.items():
        if country_info["eng"] == country_name:
            return country_info
    return None


def get_numbers_v2(country_id: int ,application_id: int):
    # The target API you want to access for getting a number
    token="mwCLHHjqs8f-M9bHZ6Bo8srAXCojX6Rn"
    target_url = f"https://api.sms-man.com/control/get-number?token={token}&country_id={country_id}&application_id={application_id}"
    response = requests.get(target_url)
    return response.json()

def get_sms_v2(request_id: int):
    count_status = 0
    code = ""
    sms=""
    # while(True):
    while count_status < 5:
    # The target API you want to access for getting SMS
        token="mwCLHHjqs8f-M9bHZ6Bo8srAXCojX6Rn"
        target_url = f"https://api.sms-man.com/control/get-sms?token={token}&request_id={request_id}"
        response = requests.get(target_url)
        sms= response.json()
        try:
            if sms['error_code'] == "wait_sms":
                time.sleep(10)
                count_status=count_status+1
                continue
        except Exception as e:
            print("An error occurred:", e)
            return sms
        else:
            return sms
    return ''        