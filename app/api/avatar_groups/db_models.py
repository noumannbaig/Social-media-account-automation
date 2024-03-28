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
)
from sqlalchemy.orm import synonym, relationship
from app.database.core import Base, TableBase


class AvatarGroup(Base, TableBase):
    __tablename__ = "avatar_groups"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    group_name = Column(String(250), nullable=False, comment="name of group")
    group_desc = Column(String(500), nullable=False, comment="description of group")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )
    creation_date = Column(
        DateTime,
        nullable=False,
        server_default=text("LOCALTIMESTAMP"),
        comment="time of record creation",
    )

    avatars = relationship("Avatar", back_populates="avatar_group")
    # Define synonyms for column names to match naming conventions
    groupName = synonym("group_name")
    groupDesc = synonym("group_desc")
    createdBy = synonym("created_by")
    creationDate = synonym("creation_date")
