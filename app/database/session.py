"""Database session handling."""
from typing import List, Union

from .core import TableBase
from .engine import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session.

    Yields:
        (Session): Current SQLAlchemy session.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


def update_session(
    db_entity: Union[TableBase, List[TableBase]], session: Session
) -> None:
    """Updates database session with new entity/entities.

    Args:
        db_entity (Union[TableBase, List[TableBase]]):
            One or list of entities (child of TableBase).
        session (Session): Current SQLAlchemy session.
    """
    try:
        if isinstance(db_entity, list):
            session.add_all(db_entity)
            session.commit()
            for elem in db_entity:
                session.refresh(elem)
        else:
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
    except SQLAlchemyError as exc:
        session.rollback()
        # reraise to allow error handlers to catch exceptions
        raise exc


def delete_entity(db_entity: TableBase, session: Session) -> None:
    """Deletes entity from database session.

    Args:
        db_entity (TableBase): An entity (child of TableBase).
        session (Session): Current SQLAlchemy session.
    """

    session.delete(db_entity)
    session.commit()
