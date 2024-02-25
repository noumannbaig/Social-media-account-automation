"""Common models and envelopes"""
# pylint: disable=no-self-argument
# Pylint disabled for validator decorator
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Generic, List, Optional, TypeVar

from fastapi import status
from pydantic import BaseModel, Field, conint, validator
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class ErrorStatus(str, Enum):
    """Enum for error specification."""

    CANCELLED = "CANCELLED"
    UNKNOWN = "UNKNOWN"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED"
    FAILED_PRECONDITION = "FAILED_PRECONDITION"
    ABORTED = "ABORTED"
    OUT_OF_RANGE = "OUT_OF_RANGE"
    UNIMPLEMENTED = "UNIMPLEMENTED"
    INTERNAL = "INTERNAL"
    UNAVAILABLE = "UNAVAILABLE"
    DATA_LOSS = "DATA_LOSS"


def to_camel(string: str) -> str:
    """Helper function to convert snake_case to camelCase.

    Args:
        string (str): Snake case input string.

    Returns:
        str: Camel case output string
    """
    return "".join(
        (word.capitalize() if i else word.lower())
        for (i, word) in enumerate(string.split("_"))
    )


class MetaInfoModel(BaseModel):
    """Model extension for including meta information
    like creation_time and update_time.
    Includes alias generator that creates aliases in camelCase"""

    create_time: datetime
    update_time: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ResponseError(BaseModel):
    """Response error model"""

    id: uuid.UUID
    timestamp: datetime
    code: int
    message: str
    status: ErrorStatus
    details: Optional[List[Any]]


class BadRequest(ResponseError):
    code = status.HTTP_400_BAD_REQUEST
    message = "Bad Request."


class NotFound(ResponseError):
    code = status.HTTP_404_NOT_FOUND
    message = "Not found."


class Unauthorized(ResponseError):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized."


class Forbidden(ResponseError):
    code = status.HTTP_403_FORBIDDEN
    message = "Forbidden."


class RequestTimeout(ResponseError):
    code = status.HTTP_408_REQUEST_TIMEOUT
    message = "Request timeout."


class InternalServerError(ResponseError):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error."


class Pagination(BaseModel):
    """Pagination submodel"""

    total_pages: Optional[conint(ge=0)] = None
    total_elements: Optional[conint(ge=0)] = None
    size: Optional[conint(gt=0)] = None
    page: Optional[conint(gt=0)] = None
    order_by: Optional[str] = None

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ResponseEnvelope(GenericModel, Generic[DataT]):
    """Envelope for all responses"""

    data: Optional[DataT]
    error: Optional[ResponseError]
    
    pagination: Optional[Pagination]

    @validator("error", always=True)
    def check_consistency(cls, error, values):
        data = values.get("data")
        if error is not None and data is not None:
            raise ValueError("Must not provide both data and error!")
        if error is None and data is None:
            raise ValueError("Must provide data or error!")
        return error

    class Config:
        allow_population_by_field_name = True


class GenericFilterParameters(BaseModel):
    """Model for generic filter query string."""

    filter: Optional[str] = None


class OrderParameters(BaseModel):
    """Parameters for ordering.

    Attributes:
        order_by (Optional[str]): Field to order by. Defaults to an empty string
            for default value.
    """

    # setting default here includes it in response envelope
    order_by: Optional[str] = Field(default="createTime:desc", alias="orderBy")

    class Config:
        allow_population_by_field_name = True


class PaginationParameters(BaseModel):
    """Parameters for pagination.

    Attributes:
        page (Optional[conint]): Page of elements. Defaults to 1.
        size (Optional[conint]): Number of elements to retrieve. Defaults to 10.
    """

    page: Optional[conint(gt=0)] = 1
    size: Optional[conint(gt=0)] = 25
