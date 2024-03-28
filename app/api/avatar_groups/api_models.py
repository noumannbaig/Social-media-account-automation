import uuid
import re
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from enum import Enum
from app.api.commons.api_models import to_camel
from typing import Optional


class AvatarGroupBase(BaseModel):
    """AvatarGroup base model."""

    group_name: str
    group_desc: str


class ValidatedContactUsFormBase(AvatarGroupBase):
    """Contact Form validation base model."""

    @validator("group_name")
    def name_alphanum(cls, v):
        assert 1 <= len(v) <= 50, "must have between 1 and 50 characters"
        assert re.fullmatch(r"^[A-Za-z0-9 ]+$", v), "must be alphanumeric"
        return v

    @validator("group_desc")
    def organization_name_alphanum(cls, v):
        assert re.fullmatch(
            r"[A-Za-z0-9\s/()_!:-@%$#&^*+><?~`,.|;'=]*", v
        ), "must be alphanumeric or special characters"
        return v


class AvatarGroupBaseInsert(ValidatedContactUsFormBase):
    """Contact Us base model for create operation."""

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True


class AvatarGroupResponse(AvatarGroupBase):
    """ContactUs form model for read operations."""

    id: int
    creation_date: datetime

    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True
