import uuid
import re
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from enum import Enum
from app.api.commons.api_models import to_camel
from typing import Optional



class CountriesBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True



class PlatformsBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True


class ProvidersBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True



class NationalityBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True



class GenderBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True



class LanguageBase(BaseModel):
    id:int
    desc_en:str
    desc_ar:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True

