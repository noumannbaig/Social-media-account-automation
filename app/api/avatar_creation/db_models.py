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


class Avatar(Base, TableBase):
    __tablename__ = "avatars"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    first_name = Column(String(250), nullable=False, comment="first name")
    last_name = Column(String(250), nullable=False, comment="last name")
    birthdate = Column(DateTime, nullable=False, comment="birth date ")
    job_title = Column(String(150), nullable=False, comment="job title")
    gender_id = Column(
        BigInteger,
        ForeignKey("genders.id"),
        nullable=False,
        comment="identity record of gender",
    )
    relationship_status_id = Column(
        BigInteger,
        ForeignKey("relationship_statuses.id"),
        nullable=False,
        comment="identity record of relationship status",
    )
    country_id = Column(
        BigInteger,
        ForeignKey("countries.id"),
        nullable=False,
        comment="identity record of country",
    )
    nationality_id = Column(
        BigInteger,
        ForeignKey("nationalities.id"),
        nullable=False,
        comment="identity record of nationality",
    )
    avatar_group_id = Column(
        BigInteger,
        ForeignKey("avatar_groups.id"),
        nullable=False,
        comment="identity record of avatar group",
    )
    bio = Column(Text, nullable=False, comment="biographical profile")
    photo = Column(String(1000), comment="storage url for profile picture")
    is_auto = Column(
        Boolean,
        nullable=False,
        server_default=text("false"),
        comment="generated automatically?",
    )
    scheduler_no = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), comment="scheduler number")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )

    # creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')
    avatar_emails= relationship("AvatarEmails",back_populates="avatars")
    avatar_languages= relationship("AvatarLanguage",back_populates="avatars")
    avatar_platforms= relationship("AvatarPlatform",back_populates="avatars")

    avatar_group = relationship("AvatarGroup", back_populates="avatars")
    country = relationship("Countries", back_populates="avatars")
    gender = relationship("Genders", back_populates="avatars")
    nationality = relationship("Nationalities", back_populates="avatars")
    relationship_status = relationship("RelationshipStatuses", back_populates="avatars")

    # firstName = synonym("first_name")
    # lastName = synonym("last_name")
    # jobTitle = synonym("job_title")
    # createdBy = synonym("created_by")
    # creationDate = synonym("creation_date")

class AvatarEmails(Base,TableBase):
    __tablename__ = 'avatar_emails'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='identity of record')
    avatar_id = Column(BigInteger, ForeignKey('avatars.id'), nullable=False, comment='identity record of avatar')
    username = Column(String(50), nullable=False, comment='username')
    password = Column(String(100), nullable=False, comment='password')
    email_provider_id = Column(BigInteger, ForeignKey('email_providers.id'), nullable=False, comment='foreign key to email provider')
    email_status_id = Column(BigInteger, ForeignKey('email_statuses.id'), nullable=False, comment='foreign key to email status')
    last_validation = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), comment='timestamp of the last validation')
    is_valid = Column(Boolean, nullable=False, server_default=text('false'), comment='is valid?')

    is_auto = Column(Boolean, nullable=False, server_default=text('false'), comment='is automated?')
    scheduler_no = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'), comment='scheduler number')
    version = Column(Integer, nullable=False, server_default=text('0'), comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    app_password = Column(String(100), nullable=False, comment='application specific password')

    avatars = relationship("Avatar", back_populates="avatar_emails")
    email_provider = relationship("EmailProviders", back_populates='avatar_emails')
    email_status = relationship("EmailStatuses", back_populates='avatar_emails')

class AvatarLanguage(Base,TableBase):
    __tablename__ = 'avatar_languages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, name='id')
    avatar_id = Column(BigInteger, ForeignKey('avatars.id'), nullable=False)  # assuming 'avatars' is the table name for avatars
    language_id = Column(BigInteger, ForeignKey('languages.id'), nullable=False)  # assuming 'languages' is the table name for languages
    version = Column(Integer, nullable=False, name='version')
    created_by = Column(BigInteger, nullable=False, name='created_by')

    # Define relationships (if the related tables/models exist)
    avatars = relationship('Avatar', back_populates='avatar_languages')
    languages = relationship('Language', back_populates='avatar_languages')
class Countries(Base, TableBase):
    __tablename__ = "countries"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    code = Column(String(50), nullable=False, comment="code")
    desc_en = Column(String(250), nullable=False, comment="description in english")
    desc_ar = Column(String(250), comment="description in arabic")
    is_active = Column(
        Boolean, nullable=False, server_default=text("true"), comment="is active?"
    )
    order_no = Column(Integer, nullable=False, comment="record order no")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )
    # creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')

    avatars = relationship("Avatar", back_populates="country")


class Genders(Base, TableBase):
    __tablename__ = "genders"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    code = Column(String(50), nullable=False, comment="code")
    desc_en = Column(String(250), nullable=False, comment="description in english")
    desc_ar = Column(String(250), comment="description in arabic")
    is_active = Column(
        Boolean, nullable=False, server_default=text("true"), comment="is active?"
    )
    order_no = Column(Integer, comment="record order no")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )
    # creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')
    avatars = relationship("Avatar", back_populates="gender")


class Nationalities(Base, TableBase):
    __tablename__ = "nationalities"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    code = Column(String(50), nullable=False, comment="code")
    desc_en = Column(String(250), nullable=False, comment="description in english")
    desc_ar = Column(String(250), comment="description in arabic")
    is_active = Column(
        Boolean, nullable=False, server_default=text("true"), comment="is active?"
    )
    order_no = Column(Integer, comment="record order no")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )
    # creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')

    avatars = relationship("Avatar", back_populates="nationality")


class RelationshipStatuses(Base, TableBase):
    __tablename__ = "relationship_statuses"

    id = Column(
        BigInteger, primary_key=True, autoincrement=True, comment="identity of record"
    )
    code = Column(String(50), nullable=False, comment="code")
    desc_en = Column(String(250), nullable=False, comment="description in english")
    desc_ar = Column(String(250), comment="description in arabic")
    is_active = Column(
        Boolean, nullable=False, server_default=text("true"), comment="is active?"
    )
    order_no = Column(Integer, comment="record order no")
    version = Column(
        Integer, nullable=False, server_default=text("0"), comment="version of record"
    )
    created_by = Column(
        BigInteger, nullable=False, comment="identity of user who created the record"
    )
    # creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')

    avatars = relationship("Avatar", back_populates="relationship_status")




from sqlalchemy.schema import PrimaryKeyConstraint, UniqueConstraint

class EmailProviders(Base):
    __tablename__ = 'email_providers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='email_providers_pk'),
        UniqueConstraint('code', name='email_providers_uk1'),
        {'comment': '--@@COMMENT\r\n--@@LOOKUP'}
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(String(250), nullable=False, comment='description in english')
    is_active = Column(Boolean, nullable=False, server_default=text('true'), comment='is active?')
    version = Column(Integer, nullable=False, server_default=text('0'), comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')
    desc_ar = Column(String(250), comment='description in arabic')
    order_no = Column(Integer, comment='record order no')

    avatar_emails = relationship('AvatarEmails', back_populates='email_provider')

class EmailStatuses(Base):
    __tablename__ = 'email_statuses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='email_statuses_pk'),
        UniqueConstraint('code', name='email_statuses_uk1'),
        {'comment': '--@@COMMENT\r\n--@@LOOKUP'}
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='identity of record')
    code = Column(String(50), nullable=False, comment='code')
    desc_en = Column(String(250), nullable=False, comment='description in english')
    is_active = Column(Boolean, nullable=False, server_default=text('true'), comment='is active?')
    version = Column(Integer, nullable=False, server_default=text('0'), comment='version of record')
    created_by = Column(BigInteger, nullable=False, comment='identity of user who created the record')
    creation_date = Column(DateTime, nullable=False, server_default=text('LOCALTIMESTAMP'), comment='time of record creation')
    desc_ar = Column(String(250), comment='description in arabic')
    order_no = Column(Integer, comment='record order no')

    avatar_emails = relationship('AvatarEmails', back_populates='email_status')


class Language(Base,TableBase):
    __tablename__ = 'languages'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, name='code')
    desc_en = Column(String(250), nullable=False, name='desc_en')
    desc_ar = Column(String(250), nullable=False, name='desc_ar')
    is_active = Column(Boolean, default=True, name='is_active')
    order_no = Column(Integer, nullable=True, name='order_no')
    version = Column(Integer, nullable=False, name='version')
    created_by = Column(BigInteger, nullable=False, name='created_by')

    avatar_languages = relationship('AvatarLanguage', back_populates='languages')



class AvatarPlatform(Base,TableBase):
    __tablename__ = 'avatar_platforms'

    id = Column(BigInteger, primary_key=True, autoincrement=True, name='id')
    avatar_id = Column(BigInteger, ForeignKey('avatars.id'), nullable=False)  # assuming 'avatars' is the table name for avatars
    email = Column(String(250), nullable=False, name='email')
    password = Column(String(100), nullable=False, name='password')
    platform_id = Column(BigInteger, ForeignKey('platforms.id'), nullable=False, index=True, name='platform_id')  # assuming 'platforms' is the table name for platforms
    platform_status_id = Column(BigInteger, ForeignKey('platform_statuses.id'), nullable=True, index=True, name='platform_status_id')  # assuming 'platform_status' is the table name for platform statuses
    last_validation = Column(DateTime, nullable=True, name='last_validation')
    is_auto = Column(Boolean, default=True, name='is_auto')
    scheduler_no = Column(UUID(as_uuid=True), server_default=text('uuid_generate_v4()'),nullable=False, name='scheduler_no')
    version = Column(Integer, nullable=False, name='version')
    created_by = Column(BigInteger, nullable=False, name='created_by')

    # Define relationships (if the related tables/models exist)
    avatars = relationship('Avatar', back_populates='avatar_platforms')
    platform = relationship('Platform', back_populates='avatar_platforms')
    platform_statuses = relationship('PlatformStatus', back_populates='avatar_platforms')



class PlatformStatus(Base,TableBase):
    __tablename__ = 'platform_statuses'

    id = Column(BigInteger, primary_key=True, autoincrement=True, name='id')
    code = Column(String(50), nullable=False, name='code')
    desc_en = Column(String(250), nullable=False, name='desc_en')
    desc_ar = Column(String(250), nullable=False, name='desc_ar')
    is_active = Column(Boolean, default=True, name='is_active')
    order_no = Column(Integer, name='order_no')  # nullable by default
    version = Column(Integer, nullable=False, name='version')
    created_by = Column(BigInteger, nullable=False, name='created_by')
    avatar_platforms = relationship('AvatarPlatform', back_populates='platform_statuses')


class Platform(Base,TableBase):
    __tablename__ = 'platforms'

    id = Column(BigInteger, primary_key=True, autoincrement=True, name='id')
    code = Column(String(50), nullable=False, name='code')
    desc_en = Column(String(250), nullable=False, name='desc_en')
    desc_ar = Column(String(250), nullable=False, name='desc_ar')
    is_active = Column(Boolean, default=True, name='is_active')
    order_no = Column(Integer, name='order_no')  # nullable by default
    version = Column(Integer, nullable=False, name='version')
    created_by = Column(BigInteger, nullable=False, name='created_by')
    avatar_platforms = relationship('AvatarPlatform', back_populates='platform')


class AvatarPlatformSchedule(Base):
    __tablename__ = 'avatar_platform_schedules'

    id = Column(BigInteger, primary_key=True)
    avatar_id = Column(BigInteger, nullable=False)
    platform_id = Column(BigInteger, nullable=False)
    week_day_id = Column(BigInteger, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_auto = Column(Boolean, nullable=False)
    scheduler_no = Column(UUID(as_uuid=True), nullable=False)
    version = Column(Integer, nullable=False)
    created_by = Column(BigInteger, nullable=False)
    creation_date = Column(DateTime, nullable=False)