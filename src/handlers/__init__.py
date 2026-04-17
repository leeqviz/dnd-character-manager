import logging

from fastapi import Request
from fastapi.responses import JSONResponse

log = logging.getLogger(__name__)


async def global_exception_handler(_: Request, exc: Exception):
    log.error("Global error caught: %s", exc, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error",
        },
    )
