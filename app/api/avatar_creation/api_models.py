import uuid
import re
from click import UUID
from pydantic import BaseModel, validator, EmailStr
from datetime import date, datetime
from enum import Enum
from app.api.commons.api_models import to_camel
from typing import Optional


class AvatarBase(BaseModel):
    """AvatarGroup base model."""

    first_name: str
    last_name: str
    birthdate: date
    a_age:Optional[int]
    job_title: Optional[str]
    a_gender: Optional[str]
    a_relationship_status: Optional[str]
    a_country: Optional[str]
    a_nationality: Optional[str]
    a_avatar_group: Optional[str]
    bio: str
    photo:Optional[str]
    is_auto: bool

class AvatarGmailBase(BaseModel):
    """AvatarGroup base model."""
    id:int
    username: str
    password: str
    provider: Optional[str]
    email_provider_id:Optional[int]
    is_valid: str
    last_validation: Optional[datetime]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True
class AvatarPlatformBase(BaseModel):
    """AvatarGroup base model."""
    id:int
    username: Optional[str]
    password: str
    platform_name: Optional[str]
    platform_id: Optional[int]

    is_valid: Optional[str]
    last_validation: Optional[datetime]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True
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
    bio_type: str
    style_id: str 
    age:list[int]

class AvatarGenerateManual(BaseModel):
    first_name: str
    last_name:str
    position: str
    bio: str
    country: int 
    group: int 
    platform: list[int]
    providers:list[int] 
    nationality: int 
    language: int 
    gender: int 
    bio_type: str
    style_id: str 
    age:list[int]
class AvatarDashbaord(BaseModel):
    number_of_avatars: int 
    idle: int 
    busy: int 


class ScheduleAvatarDashbaord(BaseModel):
    number_of_avatars: int 
    email_availibilty: int 
    platform_availabity: int
    errors:int