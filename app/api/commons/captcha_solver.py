import os
from twocaptcha import TwoCaptcha


def solveRecaptcha(sitekey, url):
    api_key = os.getenv('APIKEY_2CAPTCHA', '71177a9e43fb991230691b569540c153')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)

    except Exception as e:
        print(e)

    else:
        return result