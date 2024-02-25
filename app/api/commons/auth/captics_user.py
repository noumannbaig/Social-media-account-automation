from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "fullname": "admin",
                "email": "admin@captics.co",
                "password": "12345678"
            }
        }

class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "user": {
                "email": "admin@captics.co",
                "password": "12345678"
            }
        }