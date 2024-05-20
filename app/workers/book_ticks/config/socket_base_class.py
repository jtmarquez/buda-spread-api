import asyncio
from typing import Any, Awaitable, Callable
from urllib.parse import quote, urljoin
from websockets import WebSocketClientProtocol
import websockets

OnMessageFunctionCallable = Callable[[WebSocketClientProtocol], Awaitable[Any]]


class BaseWebSocket:
    def __init__(self, base_uri: str) -> None:
        self._base_uri = base_uri
        self._live_sockets: list[WebSocketClientProtocol] = []

    def _parse_uri_channels(self, uri: str, channels: list[str] = None):
        parsed_uri = uri

        if channels:
            quoted_channels = [quote(channel) for channel in channels]
            channel_param = ",".join(quoted_channels)
            parsed_uri = urljoin(parsed_uri, f"sub?channel={channel_param}")

        return parsed_uri

    async def _on_message(
        self, ws: WebSocketClientProtocol, on_msg_callback: OnMessageFunctionCallable
    ):
        if on_msg_callback:
            await on_msg_callback(ws)

    async def listen(
        self,
        on_message: OnMessageFunctionCallable,
        uri: str = None,
        channels: list[str] = None,
        ping_interval = None
    ):
        ws_uri = uri or self._base_uri

        parsed_ws_uri = self._parse_uri_channels(ws_uri, channels)

        async with websockets.connect(parsed_ws_uri, ping_interval=ping_interval) as ws:
            await self._on_message(ws, on_message)

    async def get_live_socket(self, uri: str = None):
        ws_uri = uri or self._base_uri
        live_socket = await websockets.connect(ws_uri)
        self._live_sockets.append(live_socket)
        return live_socket

    async def send_message(
        self,
        message: str,
        uri: str = None,
        existent_connection: WebSocketClientProtocol = None,
    ):
        if existent_connection:
            await existent_connection.send(message)
        else:
            ws_uri = uri or self._base_uri

            async with websockets.connect(ws_uri) as ws:
                await ws.send(message)

    async def close_existent_sockets(self):
        await asyncio.gather(*[alive_socket.close() for alive_socket in self._live_sockets])
        self._live_sockets = []
