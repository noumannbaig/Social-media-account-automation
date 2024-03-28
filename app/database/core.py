"""Setup for base model and database connection used by all defined api_models.
"""

import uuid

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TableBase:
    """Base model which defines common attributes that
    should be inherited by all database api_models."""

    creation_date = Column(
        DateTime,
        nullable=False,
        server_default=text("LOCALTIMESTAMP"),
        comment="time of record creation",
    )
