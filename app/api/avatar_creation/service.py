import csv
from io import StringIO
import select
import string
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from typing import Optional, Tuple, List
import openai
import os
import random
import httpx
import boto3
from datetime import datetime, timezone
from app.api.avatar_creation.db_models import (
    Avatar,
    AvatarEmails,
    AvatarLanguage,
    AvatarPlatform,
    Countries,
    Genders,
    Nationalities,
    RelationshipStatuses,
)
from app.api.avatar_groups.db_models import AvatarGroup
from app.api.commons.account_creation import create_gmail_account
from app.api.commons.generate_profile_picture import upload_image_to_s3
from app.api.commons.helpers import (
    clean_name,
    generate_complex_password,
    generate_profile_picture,
)
from app.api.avatar_creation.api_models import AvatarBaseInsert, AvatarEmail, AvatarGenerate, AvatarGenerateManual, AvatarPlatformAdd, AvatarPlatformBase, AvatarPlatformUpdate, AvatarGmailEdit
from app.api.jobs.db_models import Schedulers
from app.database.session import update_session, delete_entity
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    PaginationParameters,
)
import logging

logger = logging.getLogger(__name__)

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY


def create_avatar(db: Session, avatars: AvatarBaseInsert) -> Avatar:
    """Create ContactUs entity.
    Args:
        session (Session): Current SQLAlchemy session
        contactUs (api_models.ContactUsFormBaseInsert): Request body according to model
    Returns:
        ContactUs: Newly created entity
    """
    meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
    db_user = Avatar(**avatars.dict(), **meta_dict, created_by=1)
    # db_user = Avatar(
    #     first_name=avatars.first_name,
    #     last_name=avatars.last_name,
    #     =
    #     created_by=1,
    #     **meta_dict,
    # )

    update_session(db_user, session=db)

    return db_user


def get_avatar_by_id(session: Session, id: int) -> Avatar:
    """Get avatar group entity by id.

    Args:
        session (Session): Current SQLAlchemy session.
        id (UUID): Id of an already created Avatar group entity.

    Returns:
        Avatar group: Meta data to the given Avatar group entity.
    """

    query = session.query(Avatar).filter(Avatar.id == id)

    return query.one()


def get_avatars_by_scheduler_no_api(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
    scheduler_no:UUID
) -> Tuple[List[Avatar], int, int]:
    """Get all parameter entries in database.

    Args:
        session (Session): Current SQLAlchemy session
        pagination_params (PaginationParameters): Pagination parameters.
        order_params (OrderParameters): Order parameters
        filter_params (GenericFilterParameters): Filter query string.

    Returns:
        Tuple[List[Parameter], int, int]:
            Tuple of reduced list of entries,
            total number of pages and total number of elements.
    """

    # Query to get a base query for ContactUs
    query = session.query(Avatar).filter(Avatar.scheduler_no==scheduler_no)

    # Apply filtering
    if filter_params.filter:
        conditions = []
        for field_value_pair in filter_params.filter.split(","):
            field, value = field_value_pair.split(":")
            if hasattr(Avatar, field):
                column = getattr(Avatar, field)
                conditions.append(column.ilike(f"%{value}%"))
        if conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*conditions))

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Avatar, field):
            column = getattr(Avatar, field)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)

    # Apply pagination
    offset = (pagination_params.page - 1) * pagination_params.size
    query = query.offset(offset).limit(pagination_params.size)

    # Execute the query
    contacted_users = query.all()

    # Calculate total number of pages
    total_pages = (total_count + pagination_params.size - 1) // pagination_params.size

    return contacted_users, total_pages, total_count
def get_platform_avatars(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[AvatarPlatform], int, int]:
    """Get all parameter entries in database.

    Args:
        session (Session): Current SQLAlchemy session
        pagination_params (PaginationParameters): Pagination parameters.
        order_params (OrderParameters): Order parameters
        filter_params (GenericFilterParameters): Filter query string.

    Returns:
        Tuple[List[Parameter], int, int]:
            Tuple of reduced list of entries,
            total number of pages and total number of elements.
    """

    # Query to get a base query for ContactUs
    query = session.query(AvatarPlatform).filter(AvatarPlatform.platform_id == 1 or AvatarPlatform.platform_id == 4)

    # Apply filtering
    if filter_params.filter:
        conditions = []
        for field_value_pair in filter_params.filter.split(","):
            field, value = field_value_pair.split(":")
            if hasattr(AvatarPlatform, field):
                column = getattr(AvatarPlatform, field)
                conditions.append(column.ilike(f"%{value}%"))
        if conditions:
            from sqlalchemy import and_
            query = query.filter(and_(*conditions))
    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(AvatarPlatform, field):
            column = getattr(AvatarPlatform, field)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)

    # Apply pagination
    offset = (pagination_params.page - 1) * pagination_params.size
    query = query.offset(offset).limit(pagination_params.size)

    # Execute the query
    contacted_users = query.all()

    # Calculate total number of pages
    total_pages = (total_count + pagination_params.size - 1) // pagination_params.size

    return contacted_users, total_pages, total_count
def get_gmail_avatars(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[AvatarEmails], int, int]:
    """Get all parameter entries in database.

    Args:
        session (Session): Current SQLAlchemy session
        pagination_params (PaginationParameters): Pagination parameters.
        order_params (OrderParameters): Order parameters
        filter_params (GenericFilterParameters): Filter query string.

    Returns:
        Tuple[List[Parameter], int, int]:
            Tuple of reduced list of entries,
            total number of pages and total number of elements.
    """

    # Query to get a base query for ContactUs
    query = session.query(AvatarEmails).filter(AvatarEmails.email_provider_id == 1)

    # Apply filtering
    if filter_params.filter:
        conditions = []
        for field_value_pair in filter_params.filter.split(","):
            field, value = field_value_pair.split(":")
            if hasattr(AvatarEmails, field):
                column = getattr(AvatarEmails, field)
                conditions.append(column.ilike(f"%{value}%"))
        if conditions:
            from sqlalchemy import and_
            query = query.filter(and_(*conditions))
    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(AvatarEmails, field):
            column = getattr(AvatarEmails, field)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)

    # Apply pagination
    offset = (pagination_params.page - 1) * pagination_params.size
    query = query.offset(offset).limit(pagination_params.size)

    # Execute the query
    contacted_users = query.all()

    # Calculate total number of pages
    total_pages = (total_count + pagination_params.size - 1) // pagination_params.size

    return contacted_users, total_pages, total_count
def get_avatars(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Avatar], int, int]:
    """Get all parameter entries in database.

    Args:
        session (Session): Current SQLAlchemy session
        pagination_params (PaginationParameters): Pagination parameters.
        order_params (OrderParameters): Order parameters
        filter_params (GenericFilterParameters): Filter query string.

    Returns:
        Tuple[List[Parameter], int, int]:
            Tuple of reduced list of entries,
            total number of pages and total number of elements.
    """

    # Query to get a base query for ContactUs
    query = session.query(Avatar)

    # Apply filtering
    if filter_params.filter:
        conditions = []
        for field_value_pair in filter_params.filter.split(","):
            field, value = field_value_pair.split(":")
            if hasattr(Avatar, field):
                column = getattr(Avatar, field)
                conditions.append(column.ilike(f"%{value}%"))
        if conditions:
            from sqlalchemy import and_
            query = query.filter(and_(*conditions))
    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Avatar, field):
            column = getattr(Avatar, field)
            if order == "desc":
                query = query.order_by(column.desc())
            else:
                query = query.order_by(column)

    # Apply pagination
    offset = (pagination_params.page - 1) * pagination_params.size
    query = query.offset(offset).limit(pagination_params.size)

    # Execute the query
    contacted_users = query.all()

    # Calculate total number of pages
    total_pages = (total_count + pagination_params.size - 1) // pagination_params.size

    return contacted_users, total_pages, total_count


def delete_avatar_bulk(session: Session, ids: List[int]) -> None:
    for id in ids:
        try:
            db_data = get_avatar_by_id(session, id)
            delete_entity(db_data, session)
        except Exception as e:
            logger.error(f"Error deleting avatar with ID: {id}. Error: {str(e)}")
    session.commit()  # Make sure to commit the session after making changes


def delete_avatar(session: Session, id: int) -> None:
    """Delete a single Avatar entity.

    Args:
        session (Session): Current SQLAlchemy session.
        id (int): Id of an already existing Avatar entity.
    """
    db_data = get_avatar_by_id(session, id)
    delete_entity(db_data, session)
    session.commit()        
        
    

def update_avatar(
    session: Session,
    id: UUID,
    contact_update: AvatarBaseInsert,
) -> Avatar:
    """Update a contactUS entity.

    Args:
        session (Session): Current SQLAlchemy session.
        id (UUID): Id of an existing  entity.
        contact_update (ContactUsFormBaseInsert):
            Request body according to model.

    Returns:
        (ContactUs): Updated entity
    """
    db_data = get_avatar_by_id(session, id)
    for key, value in contact_update.dict(exclude_unset=True).items():
        setattr(db_data, key, value)
        update_session(db_data, session)
    return db_data


def generate_users(
    session: Session,
    number_of_users: int,
    country: str,
    group=None,
    platform=None,
    nationality=None,
    language=None,
    gender=None,
    style_id="default",
):
    users = []
    country_id = session.query(Countries).filter(Countries.desc_en == country).first()
    gender_id = session.query(Genders).filter(Genders.desc_en == gender).first()
    group_id = session.query(AvatarGroup).filter(AvatarGroup.group_name == group).first()
    nationalities_id = session.query(Nationalities).filter(
        Nationalities.desc_en == nationality
    ).first()
    try:
        for _ in range(number_of_users):

            first_name_prompt = f"Generate a common first name {gender} in {country}:"
            last_name_prompt = f"Generate a common last name in {country}:"

            # Use custom prompts for generating first and last names
            first_name_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=first_name_prompt,
                max_tokens=5,
            )
            first_name = clean_name(first_name_response.choices[0].text.strip())

            last_name_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=last_name_prompt,
                max_tokens=5,
            )
            last_name = clean_name(last_name_response.choices[0].text.strip())

            bio_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=f"Write a short bio for a {gender} named {first_name} interested in {group}:",
                max_tokens=50,
            )
            bio = bio_response.choices[0].text.strip()

            position_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=f"Generate a position title for someone in the {group} group:",
                max_tokens=10,
            )
            position = position_response.choices[0].text.strip()

            relationship_status = random.choice(
                ["Single", "Married", "It's Complicated"]
            )

            full_name = f"{first_name} {last_name}"

            # Generate a username and password
            username = f"{first_name.lower()}.{last_name.lower()}{os.urandom(3).hex()}"
            email = f"{username}@gmail.com"
            password = generate_complex_password(16)

            # Generate a random birthday between 1980 and 2000
            year = random.randint(1980, 2000)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Using 28 to avoid issues with February
            birthday = datetime(year, month, day).strftime("%m/%d/%Y")
            meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
            # Prepare and insert user data
            db_user = Avatar(
                first_name=first_name,
                last_name=last_name,
                birthdate=birthday,
                job_title=position,
                gender_id=gender_id.id,  # Assuming you have a gender_id already defined
                relationship_status_id=2,  # Assuming you have a relationship_status_id defined
                country_id=country_id.id,  # Assuming you have a country_id defined
                nationality_id=nationalities_id.id,  # Assuming you have a nationality_id defined
                avatar_group_id=group_id.id,  # Assuming you have an avatar_group_id defined
                bio=bio,
                is_auto=True,  # Assuming it's not automatically generated
                version=0,  # Assuming the initial version is 0
                created_by=1,  
                **meta_dict# Assuming you have the user_id of the creator
            )
            update_session(db_user, session)

            db_avatar_emails=AvatarEmails(
                username=username,
                password=password,
                avatar_id=db_user.id,
                email_provider_id=1,
                scheduler_no=uuid.uuid1(),
                email_status_id=1,
                is_auto=True,
                is_valid=True,
                last_validation=datetime.now(),
                created_by=1,
                **meta_dict
            )
            users.append(db_user)
            update_session(db_avatar_emails, session)
        return {
            "message": f"{number_of_users} users generated successfully",
            "users": users,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def generate_users_manually(
    session: Session,
    request:AvatarGenerateManual,
):
    country_entity = session.query(Countries).filter(Countries.id==request.country).first()
    gender_entity = session.query(Genders).filter(Genders.id==request.gender).first()
    group_entity = session.query(AvatarGroup).filter(AvatarGroup.id==request.group).first()
    nationality_entity = session.query(Nationalities).filter(Nationalities.id==request.nationality).first()
    relationship_status=session.query(RelationshipStatuses).filter(RelationshipStatuses.id==request.relationship_status).first()


    try:
      

        full_name = f"{request.first_name} {request.last_name}"

            # Generate a username and password
            # username = f"{first_name.lower()}.{last_name.lower()}{os.urandom(4).isdigit()}"
        username=generate_username(request.first_name,request.last_name)
        email = f"{username}@gmail.com"
        password = generate_complex_password(8)

            # Generate a random birthday between 1980 and 2000
        year = random.randint(1980, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Using 28 to avoid issues with February
        birthday = request.birthday.strftime("%m/%d/%Y")
        meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
            # Prepare and insert user data
        db_user = Avatar(
            first_name=request.first_name,
            last_name=request.last_name,
            birthdate=birthday,
            job_title=request.position,
            gender_id=request.gender,  # Assuming you have a gender_id already defined
            relationship_status_id=relationship_status.id,  # Assuming you have a relationship_status_id defined
            country_id=request.country,  # Assuming you have a country_id defined
            nationality_id=request.nationality,  # Assuming you have a nationality_id defined
            avatar_group_id=request.group,
            bio=request.bio,
            is_auto=False, 
            
            version=0,  # Assuming the initial version is 0
            created_by=1,  
            **meta_dict# Assuming you have the user_id of the creator
        )
        update_session(db_user, session)

        # db_avatar_emails=AvatarEmails(
        #     username=username,
        #     password=password,
        #     avatar_id=db_user.id,
        #     email_provider_id=1,
        #     email_status_id=1,
        #     is_auto=False,
        #     is_valid=True,
        #     last_validation=datetime.now(),
        #     created_by=1,
        #     **meta_dict
        # )
        # update_session(db_avatar_emails, session)

        db_languages=AvatarLanguage(
            avatar_id = db_user.id,
            language_id = request.language,
            version = 0,
            created_by = 1,
            **meta_dict
        )
        update_session(db_languages, session)
        # if(len(request.platform) != 0):
        #     for platform_id in request.platform:
        #         db_platform = AvatarPlatform(
        #             avatar_id=db_user.id,
        #             email=email,
        #             password=password,
        #             platform_id=platform_id,
        #             platform_status_id=1,  # Assuming a default status ID of 1 for all platforms
        #             last_validation=None,  # Assuming it's nullable and setting it to None
        #             is_auto=False,
        #             version=0,  # Assuming version starts at 0
        #             created_by=1,
        #              **meta_dict # Assuming the creator ID is 1
        #         )
        #         update_session(db_platform, session)
                    # result=create_gmail_account(first_name,last_name,username,datetime(year, month, day).strftime("%d %m %Y"),str(request.gender),password)
                    # if result is not None:
                    #     db_avatar_emails.app_password=result["password"]
                    #     db_avatar_emails.status="COMPLETED"
                    # else:
                    #     db_avatar_emails.status="FAILED"

        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def generate_user_email(
    session: Session,
    request:AvatarEmail,
):
    try:
        db_avatar= get_avatar_by_id(session,request.avatar_id)
        if db_avatar is None:
                raise HTTPException(status_code=404, detail="Avatar not found")    

        meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
            # Prepare and insert user data
        

        db_avatar_emails=AvatarEmails(
            username=request.username,
            password=request.password,
            avatar_id=db_avatar.id,
            email_provider_id=request.provider_id,
            email_status_id=1,
            is_auto=False,
            is_valid=True,
            last_validation=datetime.now(),
            created_by=1,
            **meta_dict
        )
        update_session(db_avatar_emails, session)


        return db_avatar_emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
def generate_user_platform(
    session: Session,
    request:AvatarPlatformAdd,
):
    try:
        db_avatar= get_avatar_by_id(session,request.avatar_id)
        if db_avatar is None:
                raise HTTPException(status_code=404, detail="Avatar not found")    

        meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
            # Prepare and insert user data
        
        db_avatar_platform=[]
        if(len(request.platform_id) != 0):
            for platform_id in request.platform_id:
                db_platform = AvatarPlatform(
                    avatar_id=db_avatar.id,
                    email=request.username,
                    password=request.password,
                    platform_id=platform_id,
                    platform_status_id=1,  # Assuming a default status ID of 1 for all platforms
                    last_validation=None,  # Assuming it's nullable and setting it to None
                    is_auto=False,
                    version=0,  # Assuming version starts at 0
                    created_by=1,
                     **meta_dict # Assuming the creator ID is 1
                )
                update_session(db_platform, session)
                db_avatar_platform.append(db_platform)
        update_session(db_platform, session)


        return db_avatar_platform
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
def get_avatars_by_scheduler_no(
    session: Session,
    scheduler_no: UUID
) -> List[Avatar]:

    # Query to get a base query for ContactUs
    query = session.query(Avatar).filter(Avatar.scheduler_no==scheduler_no).all()
    return query

def get_avatars_platforms_by_scheduler_no(
    session: Session,
    scheduler_no: UUID
) -> List[AvatarPlatform]:

    # Query to get a base query for ContactUs
    query = session.query(AvatarPlatform).filter(AvatarPlatform.scheduler_no==scheduler_no).all()
    return query

def generate_username(first_name, last_name):
    # Generate a random 4-character alphanumeric string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    username = f"{first_name.lower()}.{last_name.lower()}{suffix}"
    return username
def generate_users_v2(
    session: Session,
    request:AvatarGenerate,
    scheduler: Optional[Schedulers]
):
    users = []
    country_entity = session.query(Countries).filter(Countries.id==request.country).first()
    gender_entity = session.query(Genders).filter(Genders.id==request.gender).first()
    group_entity = session.query(AvatarGroup).filter(AvatarGroup.id==request.group).first()
    nationality_entity = session.query(Nationalities).filter(Nationalities.id==request.nationality).first()
    db_relationship_status=session.query(RelationshipStatuses).filter(RelationshipStatuses.id.in_(request.relationship_status)).all()
    query = session.query(Avatar).all()
    
    
    # Execute the query
    
    # Fetch all the first names from the result
    first_names = [row.first_name for row in query]    
    try:
        for _ in range(request.number_of_users):

            first_name_prompt = f"Generate a Unique first name {gender_entity.desc_en} in {country_entity.desc_en} exclclude all the names present in list provided {first_names}:"
            last_name_prompt = f"Generate a Unique max 7 charcthers last name in {country_entity.desc_en}:"

            # Use custom prompts for generating first and last names
            first_name_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=first_name_prompt,
                max_tokens=5,
            )
            first_name = clean_name(first_name_response.choices[0].text.strip())

            last_name_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=last_name_prompt,
                max_tokens=5,
            )
            last_name = clean_name(last_name_response.choices[0].text.strip())

            bio_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=f"Write a Short {request.bio_type} bio for a {gender_entity.desc_en} named {first_name} interested in {group_entity.groupDesc} with max 15 words:",
                max_tokens=50,
            )
            bio = bio_response.choices[0].text.strip()

            position_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct-0914",
                prompt=f"Generate a Random position title for someone in the {group_entity}:",
                max_tokens=10,
            )
            position = position_response.choices[0].text.strip()

            relationship_status = random.choice(
                db_relationship_status
            )

            full_name = f"{first_name} {last_name}"

            # Generate a username and password
            # username = f"{first_name.lower()}.{last_name.lower()}{os.urandom(4).isdigit()}"
            username=generate_username(first_name,last_name)
            email = f"{username}@gmail.com"
            password = generate_complex_password(8)

            # Generate a random birthday between 1980 and 2000
            year = random.randint(1980, 2000)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Using 28 to avoid issues with February
            birthday = datetime(year, month, day).strftime("%m/%d/%Y")
            meta_dict = dict(
        creation_date=datetime.now(timezone.utc),
    )
            if scheduler is not None:
            # Prepare and insert user data
                db_user = Avatar(
                    first_name=first_name,
                    last_name=last_name,
                    birthdate=birthday,
                    job_title=position,
                    gender_id=request.gender,  # Assuming you have a gender_id already defined
                    relationship_status_id=relationship_status.id,  # Assuming you have a relationship_status_id defined
                    country_id=request.country,  # Assuming you have a country_id defined
                    nationality_id=request.nationality,  # Assuming you have a nationality_id defined
                    avatar_group_id=request.group,
                    bio=bio,
                    is_auto=True, 
                    scheduler_no=scheduler.scheduler_no, 
                    version=0,  # Assuming the initial version is 0
                    created_by=1,  
                    **meta_dict# Assuming you have the user_id of the creator
                )
                update_session(db_user, session)
            else:
                db_user = Avatar(
                    first_name=first_name,
                    last_name=last_name,
                    birthdate=birthday,
                    job_title=position,
                    gender_id=request.gender,  # Assuming you have a gender_id already defined
                    relationship_status_id=2,  # Assuming you have a relationship_status_id defined
                    country_id=request.country,  # Assuming you have a country_id defined
                    nationality_id=request.nationality,  # Assuming you have a nationality_id defined
                    avatar_group_id=request.group,
                    bio=bio,
                    is_auto=True, 
                    version=0,  # Assuming the initial version is 0
                    created_by=1,  
                    **meta_dict# Assuming you have the user_id of the creator
                )
                update_session(db_user, session)

            db_avatar_emails=AvatarEmails(
                username=username,
                password=password,
                avatar_id=db_user.id,
                email_provider_id=1,
                scheduler_no=scheduler.scheduler_no,
                email_status_id=1,
                is_auto=True,
                is_valid=True,
                last_validation=datetime.now(),
                created_by=1,
                **meta_dict
            )
            users.append(db_user)
            update_session(db_avatar_emails, session)

            db_languages=AvatarLanguage(
                avatar_id = db_user.id,
                language_id = request.language,
                version = 0,
                created_by = 1,
                **meta_dict
            )
            update_session(db_languages, session)
            if(len(request.platform) != 0):
                for platform_id in request.platform:
                    db_platform = AvatarPlatform(
                        avatar_id=db_user.id,
                        email=email,
                        password=password,
                        platform_id=platform_id,
                        platform_status_id=1,  # Assuming a default status ID of 1 for all platforms
                        last_validation=None,  # Assuming it's nullable and setting it to None
                        is_auto=True,
                        scheduler_no=scheduler.scheduler_no,
                        version=0,  # Assuming version starts at 0
                        created_by=1,
                         **meta_dict # Assuming the creator ID is 1
                    )
                    update_session(db_platform, session)
                    # result=create_gmail_account(first_name,last_name,username,datetime(year, month, day).strftime("%d %m %Y"),str(request.gender),password)
                    # if result is not None:
                    #     db_avatar_emails.app_password=result["password"]
                    #     db_avatar_emails.status="COMPLETED"
                    # else:
                    #     db_avatar_emails.status="FAILED"


        return {
            "message": f"{request.number_of_users} users generated successfully",
            "users": users,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_avatars_by_scheduler_no(
    session: Session,
    scheduler_no: UUID
) -> List[Avatar]:

    # Query to get a base query for ContactUs
    query = session.query(Avatar).filter(Avatar.scheduler_no==scheduler_no).all()
    return query

def get_avatars_platforms_by_scheduler_no(
    session: Session,
    scheduler_no: UUID
) -> List[AvatarPlatform]:

    # Query to get a base query for ContactUs
    query = session.query(AvatarPlatform).filter(AvatarPlatform.scheduler_no==scheduler_no).all()
    return query

def generate_username(first_name, last_name):
    # Generate a random 4-character alphanumeric string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    username = f"{first_name.lower()}.{last_name.lower()}{suffix}"
    return username


def upload_avatar_image(session:Session, id:int, image_bytes: bytes , file_name: str):
    avatar=get_avatar_by_id(session,id)
    try:

        profile_picture=upload_image_to_s3(image_bytes,file_name)
        avatar.photo=profile_picture
        update_session(avatar,session)
        return True
    except Exception as e:
        return False
    

def export_avatar_to_csv( db: Session):
    """Export avatar data to CSV file."""
    avatars = db.query(Avatar).all()
    if not avatars:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    # Create a StringIO object to write CSV data
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    
    # Write headers
    csv_writer.writerow(["Id", "FirstName", "LastName","Email","Password", "Birthdate", "job title", "Gender", 
                         "relationshipStatus", "Country", "Nationality", "avatar group", 
                            ])
    
    # Write data
# Write data
    for avatar in avatars:
        if len(avatar.avatar_emails)==0:
             csv_writer.writerow([
                avatar.id, avatar.first_name, avatar.last_name,
                '', '', avatar.birthdate, avatar.job_title,
                avatar.gender.desc_en, avatar.relationship_status.desc_en, 
                avatar.country.desc_en, avatar.nationality.desc_en,
                avatar.avatar_group.group_name
            ])
        else:
            for email in avatar.avatar_emails:
                csv_writer.writerow([
                    avatar.id, avatar.first_name, avatar.last_name,
                    email.username, email.password, avatar.birthdate, avatar.job_title,
                    avatar.gender.desc_en, avatar.relationship_status.desc_en, 
                    avatar.country.desc_en, avatar.nationality.desc_en,
                    avatar.avatar_group.group_name
                ])
    
    # Reset pointer to start of StringIO object
    csv_data.seek(0)
    
    return csv_data


def update_avatar_platform(
    session: Session, id: int, platform_update: AvatarPlatformUpdate
) -> str:
    try:
        platform = session.query(AvatarPlatform).filter(AvatarPlatform.id == id).one_or_none()

        if not platform:
            raise HTTPException(status_code=404, detail="Platform not found")

        # Update the specific fields
        platform.email = platform_update.email
        platform.password = platform_update.password
        platform.platform_id = platform_update.platform_id[0]  # Assuming a single platform ID

        session.commit()
        return f"Avatar platform edited successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"A programming error occurred on the database: {str(e)}")

def delete_avatar_platform(session: Session, id: int) -> str:
    platform = session.query(AvatarPlatform).filter(AvatarPlatform.id == id).one_or_none()

    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")

    session.delete(platform)
    session.commit()

    return f"Avatar platform deleted successfully"

def update_avatar_gmail(
    session: Session, id: int, gmail_update: AvatarGmailEdit
) -> str:
    """Update a Gmail account entity."""
    gmail_account = session.query(AvatarEmails).filter(AvatarEmails.id == id).one_or_none()

    if not gmail_account:
        raise HTTPException(status_code=404, detail="Gmail account not found")

    for key, value in gmail_update.dict(exclude_unset=True).items():
        setattr(gmail_account, key, value)

    session.commit()

    return f"Email edited successfully"

def delete_avatar_gmail(session: Session, id: int) -> str:
    gmail_account = session.query(AvatarEmails).filter(AvatarEmails.id == id).one_or_none()

    if not gmail_account:
        raise HTTPException(status_code=404, detail="Gmail account not found")

    session.delete(gmail_account)
    session.commit()

    return f"Email deleted successfully"