from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from typing import Tuple, List
from sqlalchemy import func,case
from enum import Enum
from pydantic import BaseModel

from datetime import datetime, timezone
from app.api.avatar_creation.db_models import Avatar, AvatarEmails, AvatarPlatform, Countries, EmailProviders, Genders, Platform, RelationshipStatuses
from app.database.session import update_session, delete_entity
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    PaginationParameters,
)
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
    uae = "United Arab Emirates"
    ksa = "Kuwait"
    qtr = "Morocco"
    usa = "United States    American"

class AgeGroupEnum(str, Enum):
    generation_x = "Generation X"
    millennials = "Millennials"
    generation_z = "Generation Z"

class RelationshipStatusEnum(str, Enum):
    married = "married"
    divorced = "divorced"
    single = "single"
    complicated = "it's complicated"
    relationship="in a relationship"

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

def get_dashboard_summary(db: Session):
    # Count total avatars
    total_avatars = db.query(func.count(Avatar.id)).scalar()

    # Status counts (assuming there are columns or ways to determine 'idle', 'busy', and 'error')
    idle_avatars = db.query(func.count(Avatar.id)).filter(Avatar.is_auto == False).scalar()
    busy_avatars = db.query(func.count(Avatar.id)).filter(Avatar.is_auto == True).scalar()
    error_avatars = 0
        # Initialize dictionaries with zero values for all enum keys
    platforms_dict = {platform: 0 for platform in PlatformEnum}
    countries_dict = {country: 0 for country in CountryEnum}
    email_providers_dict = {provider: 0 for provider in EmailProviderEnum}
    relationship_statuses_dict = {status: 0 for status in RelationshipStatusEnum}
    genders_dict = {gender: 0 for gender in GenderEnum}
    age_groups_dict = {age_group: 0 for age_group in AgeGroupEnum}
    job_titles_dict = {job_title: 0 for job_title in JobTitleEnum}
    # Platforms summary
    platforms_summary = db.query(
        Platform.desc_en,
        func.count(AvatarPlatform.id)
    ).select_from(AvatarPlatform)\
      .join(Platform, AvatarPlatform.platform_id == Platform.id)\
      .group_by(Platform.desc_en).all()
    for platform, count in platforms_summary:
            if platform in PlatformEnum.__members__.values():
                platforms_dict[PlatformEnum(platform)] = count
    # platforms_dict = {PlatformEnum(item[0]): item[1] for item in platforms_summary}  # Map to enum after fetching


    # Countries summary
    countries_summary = db.query(
        Countries.desc_en,
        func.count(Avatar.id)
    ).select_from(Avatar)\
      .join(Countries, Avatar.country_id == Countries.id)\
      .group_by(Countries.desc_en).all()
    for country, count in countries_summary:
            if country in CountryEnum.__members__.values():
                countries_dict[CountryEnum(country)] = count
    # countries_dict = {CountryEnum(item[0]): item[1] for item in countries_summary}

    # Email providers summary
    email_providers_summary = db.query(
        EmailProviders.desc_en,
        func.count(AvatarEmails.id)
    ).select_from(AvatarEmails)\
      .join(EmailProviders, AvatarEmails.email_provider_id == EmailProviders.id)\
      .group_by(EmailProviders.desc_en).all()
    for email_provider, count in email_providers_summary:
            if email_provider in EmailProviderEnum.__members__.values():
                email_providers_dict[EmailProviderEnum(email_provider)] = count
    # email_providers_dict = {EmailProviderEnum(item[0]): item[1] for item in email_providers_summary}

    # Relationship statuses summary
    relationship_statuses_summary = db.query(
        RelationshipStatuses.desc_en,
        func.count(Avatar.id)
    ).select_from(Avatar)\
      .join(RelationshipStatuses, Avatar.relationship_status_id == RelationshipStatuses.id)\
      .group_by(RelationshipStatuses.desc_en).all()
    for relation_status, count in relationship_statuses_summary:
            if relation_status in RelationshipStatusEnum.__members__.values():
                relationship_statuses_dict[RelationshipStatusEnum(relation_status)] = count
    # relationship_statuses_dict = {RelationshipStatusEnum(item[0]): item[1] for item in relationship_statuses_summary}

    # Genders summary
    genders_summary = db.query(
        Genders.desc_en,
        func.count(Avatar.id)
    ).select_from(Avatar)\
      .join(Genders, Avatar.gender_id == Genders.id)\
      .group_by(Genders.desc_en).all()
    for gender, count in platforms_summary:
            if gender in GenderEnum.__members__.values():
                genders_dict[GenderEnum(gender)] = count
    # genders_dict = {GenderEnum(item[0]): item[1] for item in genders_summary}

    # Age groups summary (this requires a custom calculation based on birthdate)
    today = func.current_date()
    age_groups_summary = db.query(
        case([
            (func.date_part('year', today) - func.date_part('year', Avatar.birthdate) < 40, AgeGroupEnum.millennials),
            (func.date_part('year', today) - func.date_part('year', Avatar.birthdate) < 60, AgeGroupEnum.generation_x),
        ], else_=AgeGroupEnum.generation_z),
        func.count(Avatar.id)
    ).group_by(case([
        (func.date_part('year', today) - func.date_part('year', Avatar.birthdate) < 40, AgeGroupEnum.millennials),
        (func.date_part('year', today) - func.date_part('year', Avatar.birthdate) < 60, AgeGroupEnum.generation_x),
    ], else_=AgeGroupEnum.generation_z)).all()
    age_groups_dict = {item[0]: item[1] for item in age_groups_summary}

    # Job titles summary
    job_titles_summary = db.query(
        Avatar.job_title,
        func.count(Avatar.id)
    ).select_from(Avatar)\
      .group_by(Avatar.job_title).all()
    job_titles_dict = {job_title: 0 for job_title in JobTitleEnum}

    # Update dictionary with counts from the database, skipping unknown job titles
    for job_title, count in job_titles_summary:
        if job_title in JobTitleEnum.__members__.values():
            job_titles_dict[JobTitleEnum(job_title)] = count
    #job_titles_dict = {JobTitleEnum(item[0]): item[1] for item in job_titles_summary}

    summary = AvatarSummary(
        total_avatars=total_avatars,
        idle=idle_avatars,
        busy=busy_avatars,
        error=0,
        platforms=platforms_dict,
        countries=countries_dict,
        email_providers=email_providers_dict,
        relationship_statuses=relationship_statuses_dict,
        genders=genders_dict,
        age_groups=age_groups_dict,
        job_titles=job_titles_dict,
    )
    
    return summary
