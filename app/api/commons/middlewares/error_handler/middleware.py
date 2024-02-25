"""Error handler definitions and overwrites."""
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    OperationalError,
    ProgrammingError,
    ResourceClosedError,
)
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from app.api.commons.api_models import (
    BadRequest,
    ErrorStatus,
    InternalServerError,
    NotFound,
    ResponseEnvelope,
    ResponseError,
)
from app.api.commons.middlewares.error_handler.exceptions import (
    CapticsException,
)

def add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to app.

    Args:
        app (FastAPI): FastAPI app
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Override request validation exceptions.

        Args:
            _ (Request): Request object.
            exc (RequestValidationError): RequestValidationError object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """
        error = BadRequest(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            details=jsonable_encoder(exc.errors()),
            status=ErrorStatus.INVALID_ARGUMENT,
        )

        

        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        # NOTE: logging handled individually where the exception is raised
        # so that the respective technical error may be logged
        if isinstance(exc.detail, ResponseError):
            return JSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder(
                    ResponseEnvelope(error=exc.detail), exclude_none=True
                ),
            )
        else:
            error = ResponseError(
                id=uuid.uuid4(),
                code=exc.status_code,
                message="Error.",
                timestamp=datetime.utcnow(),
                details=[exc.detail],
                status=ErrorStatus.UNKNOWN,
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=jsonable_encoder(
                    ResponseEnvelope(error=error), exclude_none=True
                ),
            )

    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(
        _: Request, exc: IntegrityError
    ) -> JSONResponse:
        """Add exception handler for IntegrityError raised by SQLAlchemy.

        Args:
            _ (Request): Request object.
            exc (IntegrityError): IntegrityError object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """

        # check for exception subtype - other types are handled by pydantic models
        switcher = {
            UniqueViolation: (
                ErrorStatus.ALREADY_EXISTS,
                "An entry with the given unique constraints already exists.",
            ),
            ForeignKeyViolation: (
                ErrorStatus.INVALID_ARGUMENT,
                "Action violates foreign key constraint.",
            ),
        }
        error_status = switcher.get(
            type(exc.orig),
            (
                ErrorStatus.UNKNOWN,
                "An unknown Integrity Error occured on the database.",
            ),
        )

        error = BadRequest(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            details=[error_status[1]],
            status=error_status[0],
        )
        
        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(NoResultFound)
    async def no_result_exception_handler(
        request: Request, exc: NoResultFound
    ) -> JSONResponse:
        """Add exception handler for NoResultFound raised by SQLAlchemy.

        Args:
            request (Request): Request object.
            _ (NoResultFound): NoResultFound object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """
        details = [f"Entity not found under path '{request.url.path}'"]
        error = NotFound(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            status=ErrorStatus.NOT_FOUND,
            details=details,
        )


        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(OperationalError)
    async def operational_error_exception_handler(
        _: Request, err: OperationalError
    ) -> JSONResponse:
        """Add exception handler for OperationalError raised by SQLAlchemy.

        Args:
            _ (Request): Request object.
            err (OperationalError): OperationalError object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """

        error_detail = "An operational error occurred on the database."
        error = InternalServerError(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            status=ErrorStatus.UNAVAILABLE,
            details=[error_detail],
        )


        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(ProgrammingError)
    async def programming_error_exception_handler(
        _: Request, err: ProgrammingError
    ) -> JSONResponse:
        """Add exception handler for ProgrammingError raised by SQLAlchemy.

        Args:
            _ (Request): Request object.
            __ (ProgrammingError): ProgrammingError object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """

        error_detail = "A programming error occurred on the database."
        error = InternalServerError(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            status=ErrorStatus.FAILED_PRECONDITION,
            details=[error_detail],
        )


        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(ResourceClosedError)
    async def resource_closed_error_exception_handler(
        _: Request, err: ResourceClosedError
    ) -> JSONResponse:
        """Add exception handler for ResourceClosedError raised by SQLAlchemy.

        Args:
            _ (Request): Request object.
            err (ResourceClosedError): ResourceClosedError object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """

        error_detail = "The database connection is closed."
        error = InternalServerError(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            status=ErrorStatus.FAILED_PRECONDITION,
            details=[error_detail],
        )


        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )

    @app.exception_handler(CapticsException)
    async def volo_query_exception_handler(
        _: Request, err: CapticsException
    ) -> JSONResponse:
        """Add exception handler for CapticsException raised by the query string parser.

        Args:
            _ (Request): Request object.
            err (CapticsException): CapticsException object.

        Returns:
            JSONResponse: ReponseEnvelope with error message.
        """

        error = BadRequest(
            id=uuid.uuid4(),
            timestamp=datetime.now(timezone.utc),
            status=ErrorStatus.INVALID_ARGUMENT,
            details=[err.args[0]],
        )


        return JSONResponse(
            status_code=error.code,
            content=jsonable_encoder(ResponseEnvelope(error=error), exclude_none=True),
        )
