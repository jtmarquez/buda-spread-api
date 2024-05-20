from starlette.config import Config

config = Config(".env")

API_VERSION: str = config("API_VERSION", default="v1")

API_HOST: str = config("API_HOST", default="0.0.0.0")

API_PORT: str = config("API_PORT", default=8000)

DATABASE_NAME: str = config("DATABASE_NAME", default="spread-api-database.db")

WS_ALLOWED_ORIGINS: str = config(
    "WS_ALLOWED_ORIGINS", default="http://localhost;https://localhost"
)
