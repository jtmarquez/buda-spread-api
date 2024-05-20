import logging
from fastapi import APIRouter, WebSocket, WebSocketException
from starlette.websockets import WebSocketDisconnect
from operator import attrgetter

from controllers.market_tick import MarketTickController


router = APIRouter()


@router.websocket_route("/")
async def websocket_ticker_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        connected_client = True
        while connected_client:
            try:
                data = await websocket.receive_json()

                if data["ev"] == "book-changed":
                    change = data["change"]
                    tick_type, value = change[:2]
                    MarketTickController.create(
                        market_pair_id=data["mk"], tick_type=tick_type, value=value
                    )
            except WebSocketDisconnect:
                logging.info("WebSocket disconnected")
                connected_client = False
            except Exception as e:
                logging.error(f"Error receiving data: {e}")
                connected_client = False
    except WebSocketException as e:
        logging.error(f"WebSocket connection error: {e}")
    except Exception as e:
        logging.error(f"Uknown websocket error: {e}")
