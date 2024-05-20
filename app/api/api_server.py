from fastapi import FastAPI

from middlewares.exceptions import ExceptionsHandlerMiddleware
from config.env_vars import API_VERSION
from middlewares.cors import CORSMiddlewareWrapper
from routes import health_routes, spread_routes, user_spread_alert_routes

api_app = FastAPI(version=API_VERSION)

api_app.add_middleware(ExceptionsHandlerMiddleware)
api_app.add_middleware(CORSMiddlewareWrapper)

api_app.include_router(health_routes.router, prefix="/health")
api_app.include_router(spread_routes.router, prefix="/spreads")
api_app.include_router(user_spread_alert_routes.router, prefix="/spread-alerts")
