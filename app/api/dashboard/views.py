from fastapi import FastAPI, HTTPException, APIRouter, Depends, Body, Response
from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.api.look_up_tables import service
from app.api.look_up_tables.api_models import CountriesBase, GenderBase, LanguageBase, NationalityBase, PlatformsBase, ProvidersBase
from app.database.session import get_db
from app.api.commons.api_models import ResponseEnvelope, status
from pydantic import BaseModel
from enum import Enum

from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    Pagination,
    PaginationParameters,
    ResponseEnvelope,
)

router = APIRouter()



class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class PlatformEnum(str, Enum):
    facebook = "Facebook"
    twitter = "Twitter"
    instagram = "Instagram"
    linkedin = "LinkedIn"

class CountryEnum(str, Enum):
    uae = "UAE"
    ksa = "KSA"
    qtr = "QTR"
    usa = "USA"

class AgeGroupEnum(str, Enum):
    generation_x = "Generation X"
    millennials = "Millennials"
    generation_z = "Generation Z"

class RelationshipStatusEnum(str, Enum):
    married = "Married"
    divorced = "Divorced"
    single = "Single"
    complicated = "Complicated"

class JobTitleEnum(str, Enum):
    ux_designer = "UX Designer"
    politician = "Politician"
    hr_manager = "HR Manager"
    influencer = "Influencer"

class EmailProviderEnum(str, Enum):
    gmail = "Gmail"
    yahoo = "Yahoo"
    outlook = "Outlook"

class AvatarSummary(BaseModel):
    total_avatars: int
    idle: int
    busy: int
    error: int
    platforms: dict[PlatformEnum, int]
    countries: dict[CountryEnum, float]
    age_groups: dict[AgeGroupEnum, float]
    genders: dict[GenderEnum, int]
    relationship_statuses: dict[RelationshipStatusEnum, float]
    job_titles: dict[JobTitleEnum, float]
    email_providers: dict[EmailProviderEnum, float]

@router.get("/dashboard/summary", response_model=AvatarSummary)
async def get_dashboard_summary():
    # This is where you would normally get your data from the database
    # For the purpose of this example, we'll use hardcoded data.
    
    summary = AvatarSummary(
        total_avatars=10000,
        idle=20,
        busy=40,
        error=60,
        platforms={
            PlatformEnum.facebook: 100,
            PlatformEnum.twitter: 350,
            PlatformEnum.instagram: 100,
            PlatformEnum.linkedin: 1000,
        },
        countries={
            CountryEnum.uae: 60,
            CountryEnum.ksa: 61,
            CountryEnum.qtr: 59,
            CountryEnum.usa: 67,
        },
        email_providers={
            EmailProviderEnum.gmail:4,
            EmailProviderEnum.outlook:0,
            EmailProviderEnum.yahoo:2,
        },
        relationship_statuses={
            RelationshipStatusEnum.married:0,
            RelationshipStatusEnum.complicated:0,
            RelationshipStatusEnum.divorced:0,
            RelationshipStatusEnum.single:0,
        },
        genders={
            GenderEnum.male:0,
            GenderEnum.female:5
        },
        age_groups={
            AgeGroupEnum.generation_x:1,
            AgeGroupEnum.generation_z:2,
            AgeGroupEnum.millennials:1,

        },
        job_titles={
            JobTitleEnum.hr_manager:1,
            JobTitleEnum.influencer:2,
            JobTitleEnum.politician:1,
            JobTitleEnum.ux_designer:2,
            
        },
        # ... additional hardcoded data would follow
    )
    
    return summary
