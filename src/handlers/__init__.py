from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import DatabaseError

from src.core import AppException, logging

log = logging.getLogger(__name__)


async def error_handler(req: Request, exc: Exception):
    log.error("Error caught: %s from %s", exc, req, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "error",
            "message": "Internal Server Error",
        },
    )


async def database_error_handler(req: Request, exc: DatabaseError):
    log.error("Database error caught: %s from %s", exc, req, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "error",
            "message": "Validation Error",
        },
    )


async def validation_error_handler(req: Request, exc: ValidationError):
    log.error("Validation error caught: %s from %s", exc, req, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "code": "error",
            "message": "Validation Error",
        },
    )


async def app_error_handler(req: Request, exc: AppException):
    log.error("App error caught: %s from %s", exc, req, exc_info=True)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.error_code,
            "message": exc.message,
        },
    )
