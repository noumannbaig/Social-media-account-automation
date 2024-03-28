from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from typing import Tuple, List

from datetime import datetime, timezone
from app.api.avatar_groups.db_models import AvatarGroup
from app.api.avatar_groups.api_models import AvatarGroupBaseInsert
from app.database.session import update_session, delete_entity
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    PaginationParameters,
)


def create_avatar_groups(db: Session, groups: AvatarGroupBaseInsert) -> AvatarGroup:
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
    db_user = AvatarGroup(
        group_name=groups.group_name,
        group_desc=groups.group_desc,
        created_by=1,
        **meta_dict,
    )

    update_session(db_user, session=db)

    return db_user


def get_avatargroup_by_id(session: Session, id: UUID) -> AvatarGroup:
    """Get avatar group entity by id.

    Args:
        session (Session): Current SQLAlchemy session.
        id (UUID): Id of an already created Avatar group entity.

    Returns:
        Avatar group: Meta data to the given Avatar group entity.
    """

    query = session.query(AvatarGroup).filter(AvatarGroup.id == id)

    return query.one()


def get_avatar_groups(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[AvatarGroup], int, int]:
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
    query = session.query(AvatarGroup)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(AvatarGroup, field):
                query = query.filter(
                    getattr(AvatarGroup, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(AvatarGroup, field):
            column = getattr(AvatarGroup, field)
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


def delete_avatar_group(session: Session, id: UUID) -> None:
    """Delete a Contact Us entity.

    Args:
        session (Session): Current SQLAlchemy session.
        definition_id (UUID): Id of an already existing FTD entity.
        id (UUID): Id of an existing contact us  entity.
    """
    db_data = get_avatargroup_by_id(session, id)
    delete_entity(db_data, session)


def update_avatar_group(
    session: Session,
    id: UUID,
    contact_update: AvatarGroupBaseInsert,
) -> AvatarGroup:
    """Update a contactUS entity.

    Args:
        session (Session): Current SQLAlchemy session.
        id (UUID): Id of an existing  entity.
        contact_update (ContactUsFormBaseInsert):
            Request body according to model.

    Returns:
        (ContactUs): Updated entity
    """
    db_data = get_avatargroup_by_id(session, id)
    for key, value in contact_update.dict(exclude_unset=True).items():
        setattr(db_data, key, value)
        update_session(db_data, session)
    return db_data
