from fastapi import HTTPException
from requests.exceptions import HTTPError

import httpx
import openai
import boto3
import requests
OPENAI_API_KEY = "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"
VYRO_API_TOKEN = "vk-JsWBLsMOPeEGpOH239dDMsqvbshykT4CAmA1l1zjXt7iGx"
BUCKET_NAME = "phazaavatars"
openai.api_key = OPENAI_API_KEY
s3_client = boto3.client(
    's3',
    aws_access_key_id ='AKIAYFBZQ5G44JVDG42C',
aws_secret_access_key='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',
)


def update_profile_picture(
    avatar_id: int, 
    style_id: int ,
    bio: str
):
    try:
        
        profile_picture_url = generate_profile_picture(avatar_id,bio, style_id)
        return {"message": "Profile picture updated successfully", "profile_picture_url": profile_picture_url}
    except Exception as e:
        return None
    

def generate_profile_picture(avatar_id: int,prompt: str, style_id: int) -> str:
    headers = {'Authorization': f'Bearer {VYRO_API_TOKEN}'}
    files = {'prompt': (None, prompt), 'style_id': (None, style_id)}
    try:
        response = requests.post('https://api.vyro.ai/v1/imagine/api/generations', headers=headers, files=files)
        response.raise_for_status()  # This will raise an HTTPError if the request returned an unsuccessful status code.
        file_name = f"profile_pictures/{avatar_id}_{style_id}.jpg"
        return upload_image_to_s3(response.content, file_name)
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6+
        raise
    except Exception as e:
        print(f"HTTP error occurred: {e}")  # Python 3.6+
        return None
        

def upload_image_to_s3(image_bytes: bytes, file_name: str) -> str:
    try:
        s3_client.put_object(Body=image_bytes, Bucket=BUCKET_NAME, Key=file_name)
        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        return image_url
    except Exception as e:
        print("Failed to upload image to S3: {e}")
        return None
        # raise HTTPException(status_code=500, detail=f"Failed to upload image to S3: {e}")