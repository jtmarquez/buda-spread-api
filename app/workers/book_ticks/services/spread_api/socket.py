from config.socket_base_class import BaseWebSocket


class SpreadAPISocket(BaseWebSocket):
    _SPREAD_API_URI = "ws://api:8000/ws/market_ticker/"

    def __init__(self) -> None:
        super().__init__(SpreadAPISocket._SPREAD_API_URI)
