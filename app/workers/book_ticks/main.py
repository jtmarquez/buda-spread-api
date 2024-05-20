import asyncio

from services.spread_api.socket import SpreadAPISocket
from services.buda.socket import BudaWebSocket
from services.buda.api import BudaAPIActions


async def get_buda_markets() -> list[str]:
    markets = await BudaAPIActions.get_markets()
    market_names = [market["name"] for market in markets["markets"]]
    return market_names


async def main():
    market_names = await get_buda_markets()
    buda_socket = BudaWebSocket()
    spread_api_socket = SpreadAPISocket()
    spread_api_live_socket = await spread_api_socket.get_live_socket()

    async def message_handler(ws):
        async for msg in ws:
            await spread_api_socket.send_message(
                msg, existent_connection=spread_api_live_socket
            )

    await buda_socket.listen_to_books(
        market_ids=market_names, on_message=message_handler
    )

    await spread_api_socket.close_existent_sockets()


if __name__ == "__main__":
    asyncio.run(main())
