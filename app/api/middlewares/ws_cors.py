from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from config.env_vars import WS_ALLOWED_ORIGINS
from config.exceptions.forbidden_origin import ForbiddenOriginException
from config.http.status_codes import StatusCodes


class WebSocketOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        if origin not in WS_ALLOWED_ORIGINS.split(";"):
            raise ForbiddenOriginException(message=f"Origin '{origin}' not allowed", status_code=StatusCodes.FORBIDDEN)
        else:
            response = await call_next(request)
            return response
