import jwt
from datetime import datetime, timedelta
from jwt import PyJWTError

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def validate_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if datetime.fromtimestamp(exp) < datetime.now():
            return None
        return payload  # or extract user details as needed
    except PyJWTError:
        return None
