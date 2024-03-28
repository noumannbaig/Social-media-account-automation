import random
import string
import boto3
from fastapi import HTTPException

BUCKET_NAME = "phazaavatars"
VYRO_API_TOKEN = "vk-JsWBLsMOPeEGpOH239dDMsqvbshykT4CAmA1l1zjXt7iGx"


def clean_name(name):
    """Remove any non-letter characters from a name."""
    return "".join(filter(str.isalpha, name))


def generate_complex_password(length=16):
    if length < 4:  # Ensure length is enough to include all types
        raise ValueError(
            "Password length must be at least 4 characters to include all character types."
        )

    # Define character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    nums = string.digits
    symbols = "!@#$%^&*()"

    # Ensure at least one character from each category
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(nums),
        random.choice(symbols),
    ]

    # Fill the rest of the password length with a mix of all characters
    all_chars = lower + upper + nums + symbols
    password += [random.choice(all_chars) for _ in range(length - 4)]

    # Shuffle the password list to mix up character types
    random.shuffle(password)

    # Convert list to string
    return "".join(password)


# AWS S3 Client Setup
s3_client = boto3.client("s3")


# Async function to upload image content to AWS S3 and return the image URL
async def upload_image_to_s3(image_bytes: bytes, file_name: str) -> str:
    try:
        s3_client.put_object(Body=image_bytes, Bucket=BUCKET_NAME, Key=file_name)
        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        return image_url
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload image to S3: {e}"
        )


# Function to generate profile picture using Vyro AI and upload it to S3
async def generate_profile_picture(prompt: str, style_id: str) -> str:
    headers = {"Authorization": f"Bearer {VYRO_API_TOKEN}"}
    files = {"prompt": (None, prompt), "style_id": (None, style_id)}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vyro.ai/v1/imagine/api/generations",
            headers=headers,
            files=files,
        )
        if response.status_code == 200:
            file_name = f"profile_pictures/{prompt}_{style_id}.jpg"
            return await upload_image_to_s3(response.content, file_name)
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to generate image with Vyro AI",
            )
