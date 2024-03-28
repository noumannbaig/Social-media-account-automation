import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import imaplib
import email
from email.header import decode_header
import re  # For regex

app = FastAPI()

class LoginCredentials(BaseModel):
    email: str
    password: str

def fetch_instagram_codes(useremail: str,password: str):
    time.sleep(15)
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(useremail, password)
        mail.select("inbox")
        
        # Fetch all emails
        status, messages = mail.search(None, 'ALL')
        if status != "OK":
            raise HTTPException(status_code=500, detail="Failed to search emails")

        instagram_codes = []

        # Regex to match the Instagram code pattern in the email subject
        code_regex = re.compile(r'\b\d{6}\b')
        time.sleep(15)

        for msg_num in messages[0].split():
            typ, msg_data = mail.fetch(msg_num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject_tuple = decode_header(msg["subject"])[0]
                    subject = subject_tuple[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(subject_tuple[1] or 'utf-8')
                    # Search for Instagram codes in the subject
                    found_codes = code_regex.findall(subject)
                    instagram_codes.extend(found_codes)

        mail.logout()
        return {"status": "success", "instagram_codes": instagram_codes}
    except imaplib.IMAP4.error:
        raise HTTPException(status_code=400, detail="IMAP login failed")


def fetch_facebook_codes(useremail: str, password: str):
    time.sleep(15)
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(useremail, password)
        mail.select("inbox")

        # Search for emails from Facebook in the inbox
        status, messages = mail.search(None, '(FROM "meta.com" SUBJECT "Facebook")')
        if status != "OK":
            raise HTTPException(status_code=500, detail="Failed to search emails")

        facebook_codes = []

        # Regex to match the Facebook code pattern in the email subject
        code_regex = re.compile(r'\b\d{5}\b')
        time.sleep(15)

        for msg_num in messages[0].split():
            typ, msg_data = mail.fetch(msg_num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject_tuple = decode_header(msg["subject"])[0]
                    subject = subject_tuple[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(subject_tuple[1] or 'utf-8')
                    # Search for Facebook codes in the subject
                    found_codes = code_regex.findall(subject)
                    facebook_codes.extend(found_codes)

        mail.logout()
        return {"status": "success", "facebook_codes": facebook_codes}
    except imaplib.IMAP4.error:
        raise HTTPException(status_code=400, detail="IMAP login failed")