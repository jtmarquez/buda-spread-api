from fastapi import FastAPI
import uvicorn

from config.env_vars import API_HOST, API_PORT, API_VERSION
from ws_server import ws_app
from api_server import api_app


app = FastAPI(version=API_VERSION)

app.mount("/api", api_app)
app.mount("/ws", ws_app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=API_HOST, port=API_PORT)
