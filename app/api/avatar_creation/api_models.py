import uuid
import re
from click import UUID
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from enum import Enum
from app.api.commons.api_models import to_camel
from typing import Optional


class AvatarBase(BaseModel):
    """AvatarGroup base model."""

    first_name: str
    last_name: str
    # birthdate: datetime
    job_title: Optional[str]
    a_gender: Optional[str]
    a_relationship_status: Optional[str]
    a_country: Optional[str]
    a_nationality: Optional[str]
    a_avatar_group: Optional[str]
    bio: str
    photo: Optional[str]
    is_auto: bool


class ValidatedAvatarBase(AvatarBase):
    """Avatar validation base model."""

    @validator("first_name", check_fields=False)
    def first_name_alphanum(cls, v):
        assert 1 <= len(v) <= 50, "must have between 1 and 50 characters"
        assert re.fullmatch(r"^[A-Za-z0-9 ]+$", v), "must be alphanumeric"
        return v

    @validator("last_name", check_fields=False)
    def last_name_alphanum(cls, v):
        assert re.fullmatch(
            r"[A-Za-z0-9\s/()_!:-@%$#&^*+><?~`,.|;'=]*", v
        ), "must be alphanumeric or special characters"
        return v


class AvatarBaseInsert(ValidatedAvatarBase):
    """Avatar base model for create operation."""

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True


class AvatarResponse(AvatarBase):
    """Avatar model for read operations."""

    id: int
    creation_date: datetime

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True


class GoogleAccount(BaseModel):
    firstName: str
    lastName: str
    Gender: str
    userName: str
    birthday: str
    password: str


class InstaAccount(BaseModel):
    email:str
    fullName: str
    userName: str
    password: str
    birthday: str
    appPassword:str

class FacebookAcount(BaseModel):
    email:str
    firstName: str
    surName: str
    password: str
    birthday: str

class AvatarGenerate(BaseModel):
    number_of_users: int 
    country: int 
    group: int 
    platform: list[int]
    providers:list[int] 
    nationality: int 
    language: int 
    gender: int 
    style_id: str 
    age:list[int]
    # @validator('age', each_item=True)
    # def check_year(cls, v):
    #     if len(str(v)) != 4:
    #         raise ValueError('Each year must be a 4-digit number')
    #     if not 1930 <= v <= 2099:  # Assuming valid years range from 1900 to 2099
    #         raise ValueError('Year must be between 1900 and 2099')
    #     return v