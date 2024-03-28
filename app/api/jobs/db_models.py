from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Boolean,
    Column,
    String,
    Text,
    Numeric,
    Enum,
    BigInteger,
    Integer,
    DateTime,
    text,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship

from sqlalchemy.orm import synonym, relationship
from app.database.core import Base, TableBase


# PHAZA.JOB_TASKS
class JobTasks(Base,TableBase):
    __tablename__ = 'job_tasks'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    job_id = Column(BigInteger, ForeignKey('jobs.id'), nullable=False, comment='identity record of job')
    task_id = Column(BigInteger, ForeignKey('tasks.id'), nullable=False, comment='identity record of task')
    task_seq = Column(Integer, nullable=False, comment='task sequence')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    jobs = relationship("Jobs", back_populates="job_tasks")
    task = relationship("Tasks", back_populates="job_tasks")
# PHAZA.JOBS
class Jobs(Base,TableBase):
    __tablename__ = 'jobs'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, unique=True, comment='code')
    desc_en = Column(Text, nullable=False, comment='description in English')
    desc_ar = Column(Text, nullable=False, comment='description in Arabic')
    job_category_id = Column(BigInteger, ForeignKey('job_categories.id'), nullable=False, comment='identity record of job category')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    job_tasks = relationship("JobTasks", back_populates="jobs")
    schedulers = relationship("Schedulers", back_populates="jobs")
# PHAZA.JOB_CATEGORIES
class JobCategories(Base,TableBase):
    __tablename__ = 'job_categories'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, unique=True, comment='code')
    desc_en = Column(Text, nullable=False, comment='description in English')
    desc_ar = Column(Text, nullable=False, comment='description in Arabic')
    is_active = Column(Boolean, server_default=text('TRUE'), nullable=False, comment='is active?')
    order_no = Column(Integer, comment='record order number')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')


class TaskCategories(Base,TableBase):
    __tablename__ = 'task_categories'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(Text, nullable=False, comment='description in English')
    desc_ar = Column(Text, nullable=True, comment='description in Arabic')
    is_active = Column(Boolean, server_default=text('TRUE'), nullable=False, comment='is active?')
    order_no = Column(Integer, comment='record order no')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')

# PHAZA.TASKS
class Tasks(Base,TableBase):
    __tablename__ = 'tasks'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(Text, nullable=False, comment='description in English')
    desc_ar = Column(Text, nullable=True, comment='description in Arabic')
    task_category_id = Column(BigInteger, ForeignKey('task_categories.id'), nullable=False, comment='identity record of task category')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    job_tasks = relationship("JobTasks", back_populates="task")
    scheduler_tasks = relationship("SchedulerTasks", back_populates="task")
# PHAZA.SCHEDULERS
class Schedulers(Base,TableBase):
    __tablename__ = 'schedulers'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    job_id = Column(BigInteger, ForeignKey('jobs.id'), nullable=True, comment='identity record of job')
    scheduler_no = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), nullable=False, unique=True, comment='scheduler number')
    start_time = Column(DateTime, nullable=True, comment='start time')
    end_time = Column(DateTime, nullable=True, comment='end time')
    scheduler_status_id = Column(BigInteger, ForeignKey('scheduler_statuses.id'), nullable=False, comment='identity record of scheduler status')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    jobs = relationship("Jobs", back_populates="schedulers")
    scheduler_tasks = relationship("SchedulerTasks", back_populates="scheduler")
    params = relationship("SchedulerParams", back_populates="scheduler")
    status = relationship("SchedulerStatuses", back_populates="scheduler")

# PHAZA.SCHEDULER_TASKS
class SchedulerTasks(Base,TableBase):
    __tablename__ = 'scheduler_tasks'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    scheduler_id = Column(BigInteger, ForeignKey('schedulers.id'), nullable=False, comment='identity record of scheduler')
    task_id = Column(BigInteger, ForeignKey('tasks.id'), nullable=False, comment='identity record of task')
    task_no = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), nullable=False, unique=True, comment='task number')
    task_seq = Column(Integer, nullable=False, comment='task sequence')
    start_time = Column(DateTime, nullable=True, comment='start time')
    end_time = Column(DateTime, nullable=True, comment='end time')
    scheduler_task_status_id = Column(BigInteger, ForeignKey('scheduler_task_statuses.id'), nullable=False, comment='identity record of job scheduler task status')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    scheduler = relationship("Schedulers", back_populates="scheduler_tasks")
    task = relationship("Tasks", back_populates="scheduler_tasks")
    status = relationship("SchedulerTaskStatuses", back_populates="scheduler_tasks")

# PHAZA.SCHEDULER_TASK_STATUSES
class SchedulerTaskStatuses(Base):
    __tablename__ = 'scheduler_task_statuses'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(String(250), nullable=False, comment='description in english')
    desc_ar = Column(String(250), nullable=True, comment='description in arabic')
    is_active = Column(Boolean, server_default=text('TRUE'), nullable=False, comment='is active?')
    order_no = Column(Integer, nullable=True, comment='record order no')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    scheduler_tasks = relationship("SchedulerTasks", back_populates="status")

# PHAZA.SCHEDULER_STATUSES (seems similar to the above, confirm if a duplicate or different)
class SchedulerStatuses(Base,TableBase):
    __tablename__ = 'scheduler_statuses'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(String(250), nullable=False, comment='description in english')
    desc_ar = Column(String(250), nullable=True, comment='description in arabic')
    is_active = Column(Boolean, server_default=text('TRUE'), nullable=False, comment='is active?')
    order_no = Column(Integer, nullable=True, comment='record order no')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    scheduler = relationship("Schedulers", back_populates="status")

# PHAZA.SCHEDULER_PARAMS
class SchedulerParams(Base,TableBase):
    __tablename__ = 'scheduler_params'
    id = Column(BigInteger, primary_key=True, nullable=False, comment='identity of record')
    scheduler_id = Column(BigInteger, ForeignKey('schedulers.id'), nullable=False, comment='identity of scheduler record')
    param_key = Column(String(100), nullable=False, comment='parameter key')
    param_value = Column(String(1000), nullable=False, comment='parameter value')
    version = Column(Integer, server_default=text('0'), nullable=False, comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    scheduler = relationship("Schedulers", back_populates="params")