from config.socket_base_class import (
    BaseWebSocket,
    OnMessageFunctionCallable,
)


class BudaWebSocket(BaseWebSocket):
    _WS_SERVER_URI = "wss://realtime.buda.com"

    def __init__(self) -> None:
        super().__init__(BudaWebSocket._WS_SERVER_URI)

    def _parse_market_ids(self, market_ids: list[str]):
        parsed_market_ids = []

        for market_id in market_ids:
            parsed_mkt_id = market_id.replace("-", "").lower()
            parsed_channel = f"book@{parsed_mkt_id}"
            parsed_market_ids.append(parsed_channel)

        return parsed_market_ids

    async def listen_to_books(
        self, market_ids: list[str], on_message: OnMessageFunctionCallable
    ):
        parsed_mkt_ids = self._parse_market_ids(market_ids)

        await self.listen(channels=parsed_mkt_ids, on_message=on_message)
