import uuid
import re
from click import UUID
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from enum import Enum
from app.api.commons.api_models import to_camel
from typing import Optional


class AddSchedulerBase(BaseModel):
    """AvatarGroup base model."""

    job_id: int
    scheduler_status_id: int



class AddSchedulerTasksBase(BaseModel):
    """AvatarGroup base model."""

    scheduler_id: int
    task_id:list[int]
class JobResponse(BaseModel):
    id: int
    code: str
    desc_en: str
    # Add other fields as needed

class SchedulerResponse(BaseModel):
    """AvatarGroup base model."""
    job:Optional[str]
    id:int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    scheduler_status:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True
class SchedulerTaskResponse(BaseModel):
    """AvatarGroup base model."""
    id:int
    task_id:Optional[int]
    task_code: Optional[str]
    start_time: Optional[datetime]
    end_time:Optional[datetime]
    scheduler_task_status_id:Optional[int]
    status_code:Optional[str]
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel
        orm_mode = True


class SchedulerDashboard(BaseModel):
    total_jobs:int
    completed:int
    pending:int
    error:int
    failed:int
