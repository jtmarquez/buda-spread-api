from fastapi import FastAPI

from config.env_vars import API_VERSION
from middlewares.ws_cors import WebSocketOriginMiddleware
from ws_routes import market_tick

ws_app = FastAPI(version=API_VERSION)

ws_app.add_middleware(WebSocketOriginMiddleware)
ws_app.include_router(market_tick.router, prefix="/market_ticker")

