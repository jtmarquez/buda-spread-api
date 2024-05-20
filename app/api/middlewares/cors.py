from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

origins = ["*"]


class CORSMiddlewareWrapper(CORSMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(
            app,
            origins,
        )
