import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, header_name: str = "X-Process-Time", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers[self.header_name] = f"{process_time:.4f}"
        return response
