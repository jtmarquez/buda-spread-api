import logging
from typing import Awaitable, Callable
from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
)
from starlette.responses import Response
from starlette.types import ASGIApp

from config.exceptions.invalid_tick_type import InvalidMarketTickType
from config.exceptions.not_found import NotFoundException
from config.exceptions.bad_request import BadRequestException
from config.exceptions.forbidden_origin import ForbiddenOriginException
from serializers.exception_serializer import ExceptionSerializer


class ExceptionsHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, dispatch: DispatchFunction | None = None) -> None:
        super().__init__(app, dispatch)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            res = await call_next(request)
            return res
        except ForbiddenOriginException as e:
            logging.error(f"Something went wrong: {e.message}")
            return ExceptionSerializer.serialize(e.message, status_code=e.status_code)
        except BadRequestException as e:
            logging.error(f"Something went wrong: {e.message}")
            return ExceptionSerializer.serialize(e.message, status_code=e.status_code)
        except NotFoundException as e:
            logging.error(f"Something went wrong: {e.message}")
            return ExceptionSerializer.serialize(e.message, status_code=e.status_code)
        except InvalidMarketTickType as e:
            logging.error(f"Something went wrong: {e.message}")
            return ExceptionSerializer.serialize(e.message, status_code=e.status_code)
        except Exception as e:
            logging.error(f"Something went wrong: {e}")
            return ExceptionSerializer.serialize("Something went wrong, try again")
