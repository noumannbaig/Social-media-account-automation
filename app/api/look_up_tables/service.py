from sqlalchemy.orm import Session
import uuid
from uuid import UUID
from typing import Tuple, List

from datetime import datetime, timezone
from app.api.avatar_creation.db_models import Countries, EmailProviders, Genders, Language, Nationalities, Platform
from app.database.session import update_session, delete_entity
from app.api.commons.api_models import (
    GenericFilterParameters,
    OrderParameters,
    PaginationParameters,
)


def get_platforms(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Platform], int, int]:
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
    query = session.query(Platform)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Platform, field):
                query = query.filter(
                    getattr(Platform, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Platform, field):
            column = getattr(Platform, field)
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


def get_providers(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[EmailProviders], int, int]:
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
    query = session.query(EmailProviders)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(EmailProviders, field):
                query = query.filter(
                    getattr(EmailProviders, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(EmailProviders, field):
            column = getattr(EmailProviders, field)
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


def get_countries(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Countries], int, int]:
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
    query = session.query(Countries)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Countries, field):
                query = query.filter(
                    getattr(Countries, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Countries, field):
            column = getattr(Countries, field)
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


def get_nationalities(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Nationalities], int, int]:
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
    query = session.query(Nationalities)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Nationalities, field):
                query = query.filter(
                    getattr(Nationalities, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Nationalities, field):
            column = getattr(Nationalities, field)
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


def get_genders(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Genders], int, int]:
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
    query = session.query(Genders)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Genders, field):
                query = query.filter(
                    getattr(Genders, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Genders, field):
            column = getattr(Genders, field)
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


def get_languages(
    session: Session,
    pagination_params: PaginationParameters,
    order_params: OrderParameters,
    filter_params: GenericFilterParameters,
) -> Tuple[List[Language], int, int]:
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
    query = session.query(Language)

    # Apply filtering
    if filter_params.filter:
        for field in filter_params.filter.split(","):
            if hasattr(Language, field):
                query = query.filter(
                    getattr(Language, field).ilike(f"%{filter_params.filter}%")
                )

    # Get total count of elements
    total_count = query.count()

    # Apply ordering
    if order_params.order_by:
        field, order = order_params.order_by.split(":")
        if hasattr(Language, field):
            column = getattr(Language, field)
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