from sched import scheduler
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from typing import Tuple, List
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
    EmailStatuses,
    Genders,
    Nationalities,
    Platform,
    RelationshipStatuses,
)
from app.api.commons.generate_profile_picture import update_profile_picture
from app.database.session import get_db

from app.api.avatar_creation.service import generate_users_v2, get_avatars_by_scheduler_no, get_avatars_platforms_by_scheduler_no
from app.api.avatar_groups.db_models import AvatarGroup
from app.api.commons.account_creation import create_gmail_account
from app.api.commons.helpers import (
    clean_name,
    upload_image_to_s3,
    generate_complex_password,
    generate_profile_picture,
)
from app.api.avatar_creation.api_models import AvatarBaseInsert, AvatarGenerate
from app.api.commons.insta_account import create_insta_account
from app.api.jobs.api_models import AddSchedulerBase, AddSchedulerTasksBase
from app.api.jobs.db_models import JobTasks, Jobs, SchedulerParams, SchedulerStatuses, SchedulerTaskStatuses, SchedulerTasks, Schedulers
from app.database.session import update_session, delete_entity
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    PaginationParameters,
)

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY




def initiate_avatar_generation(db: Session, params: dict):
    # Step 1: Required Parameters are already provided as `params`

    # Step A: Find Job
    job = db.query(Jobs).filter(Jobs.code == "GenerateAvatar").first()
    if not job:
        raise ValueError("Job not found")

    # Step B: Find Job Tasks
    job_tasks_list = db.query(JobTasks).filter(JobTasks.job_id == job.id).all()

    # Step C: Find Pending Scheduler Status
    scheduler_status_pending = db.query(SchedulerStatuses).filter(SchedulerStatuses.code == "Pending").first()

    # Step D: Find Pending Scheduler Task Status
    scheduler_task_status_pending = db.query(SchedulerTaskStatuses).filter(SchedulerTaskStatuses.code == "Pending").first()
    meta_dict = dict(
            creation_date=datetime.now(timezone.utc),
        )
    # Step E: Add Scheduler
    scheduler = Schedulers(
        job_id=job.id,
        scheduler_status_id=scheduler_status_pending.id,
        scheduler_no=uuid.uuid4(),
        **meta_dict,
        created_by=1,
        # start_time and end_time can be set according to the requirements
    )
    update_session(scheduler, session=db)

    meta_dict = dict(
            creation_date=datetime.now(timezone.utc),
        )
    # Step F: Add Scheduler Tasks
    scheduler_task_list = []
    for job_task in job_tasks_list:
        scheduler_task = SchedulerTasks(
            scheduler_id=scheduler.id,
            task_id=job_task.task_id,
            scheduler_task_status_id=scheduler_task_status_pending.id,
            task_no=uuid.uuid4(),
            task_seq=job_task.task_seq,
            **meta_dict,
            created_by=1,
            # start_time and end_time can be set according to the requirements
            # task_seq can be set according to the requirements
        )
        scheduler_task_list.append(scheduler_task)
    update_session(scheduler_task_list, session=db)

    # Step G: Add Scheduler Parameters
    for key, value in params.items():
        scheduler_param = SchedulerParams(
            scheduler_id=scheduler.id,
            param_key=key,
            param_value=value,
            created_by=1,
            # Other fields like `created_by` can be set according to the context
        )
        update_session(scheduler_param, session=db)
    #process_scheduler_tasks(db,scheduler)
    return {"message": "Avatar generation initiated", "scheduler_id": scheduler.id}


def handle_task_code(db: Session,task_code: str, scheduler: Schedulers,avatar_generate_data: AvatarGenerate):
    users=get_avatars_by_scheduler_no(db,scheduler.scheduler_no)
    if task_code == "GenerateAvatarProfile":
        avatar_profiles=generate_users_v2(db,avatar_generate_data,scheduler)
    elif task_code == "GenerateAvatarPhoto":
        for user in users:
            profile_pic=update_profile_picture(user.id,21,user.bio)
            user.photo=profile_pic['profile_picture_url']
            update_session(user,session=db)
            
    elif task_code == "GenerateAvatarEmail":
        # Add the actual implementation for generating the avatar email
        for user in users:
            username=db.query(AvatarEmails).filter(AvatarEmails.avatar_id==user.id).first()
            response_gmail=create_gmail_account(user.first_name,user.last_name,username.username,f"{user.birthdate.day} {user.birthdate.month} {user.birthdate.year}",str(user.gender.id),username.password)
            if response_gmail is None:
                retry_count=5
                for count in range(retry_count):
                    retry_response_gmail=create_gmail_account(user.first_name,user.last_name,user.avatar_emails.username,f"{user.birthdate.day} {user.birthdate.month} {user.birthdate.year}",str(user.gender.id),user.avatar_emails.password)
                    count=count+1
                    if retry_response_gmail is None:
                        continue
            if response_gmail !=None:
                # username.app_password=response_gmail['password']
                username.is_valid=True
                status=db.query(EmailStatuses).filter(EmailStatuses.code=="Created").first()
                username.email_status_id=status.id
                
                update_session(user,session=db)
                update_session(username,session=db)

            continue

    elif task_code == "GenerateAvatarPlatform":
        platforms=get_avatars_platforms_by_scheduler_no(db,scheduler.scheduler_no)
        for platform in platforms:
            existing_platforms=db.query(Platform).filter(Platform.id==platform.platform_id).first()
            if existing_platforms.desc_en=="Instagram":
                for user in users:
                    username=db.query(AvatarEmails).filter(AvatarEmails.avatar_id==user.id).first()
                    if not username.app_password:
                        continue
                    insta_response=create_insta_account(username.username,f"{user.first_name} {user.last_name}",username.password,f"{user.birthdate.day} {user.birthdate.month} {user.birthdate.year}",username.app_password)
            elif existing_platforms.desc_en=="Facebook":
                continue
    else:
        raise ValueError(f"Unrecognized task code: {task_code}")

def process_scheduler_tasks(db: Session, scheduler: Schedulers):
    # Find Scheduler Tasks ordered by task sequence
    scheduler_running = db.query(SchedulerStatuses).filter(SchedulerStatuses.code == "Running").first()

    scheduler.start_time= datetime.now()
    scheduler.scheduler_status_id=scheduler_running.id,
    update_session(scheduler,db)
    tasks = db.query(SchedulerTasks).filter(SchedulerTasks.scheduler_id == scheduler.id).order_by(SchedulerTasks.task_seq).all()
    params= db.query(SchedulerParams).filter(SchedulerParams.scheduler_id==scheduler.id).all()
    data = {}
    for param in params:
        # Check for array-like strings and parse them
        if param.param_key in ['platform', 'providers', 'age']:
            data[param.param_key] = parse_pg_array(param.param_value)
        else:
            # For other types, attempt direct conversion
            data[param.param_key] = int(param.param_value) if param.param_value.isdigit() else param.param_value
    avatar_generate_data = AvatarGenerate(**data)
    for task in tasks:
        # Update Scheduler Task Status to Running
        task_status_running = db.query(SchedulerTaskStatuses).filter(SchedulerTaskStatuses.code == "Running").first()
        task.scheduler_task_status_id = task_status_running.id
        task.start_time = datetime.now()
        update_session(task,db)

        try:
            # Execute the task based on the task code
            handle_task_code(db,task.task.code, scheduler,avatar_generate_data) 

            # Update Scheduler Task Status to Completed
            task_status_completed = db.query(SchedulerTaskStatuses).filter(SchedulerTaskStatuses.code == "Completed").first()
            task.scheduler_task_status_id = task_status_completed.id
        except Exception as e:
            # Update Scheduler Task Status to Failed
            task_status_failed = db.query(SchedulerTaskStatuses).filter(SchedulerTaskStatuses.code == "Failed").first()
            task.scheduler_task_status_id = task_status_failed.id

        task.end_time = datetime.now()
        update_session(task,db)

def run_avatar_generation_scheduler():
    # Find All Pending Schedulers
    db = next(get_db())
    try:
        pending_schedulers = db.query(Schedulers).filter(
            Schedulers.scheduler_status_id == db.query(SchedulerStatuses).filter(
                SchedulerStatuses.code == "Pending"
            ).first().id
        ).all()
        print("schedulers to process.",pending_schedulers)

        if not pending_schedulers:
            print("No schedulers to process.")
            return "No schedulers to process."

        for scheduler in pending_schedulers:
            # Update Scheduler Status to Running
            scheduler_status_running = db.query(SchedulerStatuses).filter(SchedulerStatuses.code == "Running").first()
            scheduler.scheduler_status_id = scheduler_status_running.id
            scheduler.start_time = datetime.now()
            update_session(scheduler,db)
            process_scheduler_tasks(db, scheduler)

            # Update Scheduler Status to Completed or Failed based on the tasks outcomes
            if all(task.scheduler_task_status_id == db.query(SchedulerTaskStatuses).filter(SchedulerTaskStatuses.code == "Completed").first().id for task in scheduler.scheduler_tasks):
                scheduler_status_completed = db.query(SchedulerStatuses).filter(SchedulerStatuses.code == "Completed").first()
                scheduler.scheduler_status_id = scheduler_status_completed.id
            else:
                scheduler_status_failed = db.query(SchedulerStatuses).filter(SchedulerStatuses.code == "Failed").first()
                scheduler.scheduler_status_id = scheduler_status_failed.id

            scheduler.end_time = datetime.now()
            db.commit()
    finally:
        db.close()

    return "Avatar generation schedulers processed."

def get_all_schedulers(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Schedulers], int, int]:
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
    query = session.query(Schedulers)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Schedulers, field):
                query = query.filter(
                    getattr(Schedulers, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Schedulers, field):
            column = getattr(Schedulers, field)
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

def get_schedulerTask_by_Schedulerid(session: Session, id: UUID) -> List[SchedulerTasks]:
    """Get avatar group entity by id.

    Args:
        session (Session): Current SQLAlchemy session.
        id (UUID): Id of an already created Avatar group entity.

    Returns:
        Avatar group: Meta data to the given Avatar group entity.
    """

    query = session.query(SchedulerTasks).filter(SchedulerTasks.scheduler_id == id)

    return query.all()

def parse_pg_array(pg_array_string: str) -> List[int]:
    # Trim the curly braces and split the string into a list
    return [int(item) for item in pg_array_string.strip('{}').split(',') if item]