from utils.date_to_string import string_to_date
from services.market_ask.model import MarketAsk
from services.market_bid.model import MarketBid


class MarketSpread:
    def __init__(self, bid: MarketBid, ask: MarketAsk):
        self.bid = bid
        self.ask = ask
        self.spread = self.ask.value - self.bid.value
        self.calculated_at = max(bid.created_at, ask.created_at)

    def serialize(self):
        return {
            "spread": self.spread,
            "bid": self.bid.serialize(),
            "ask": self.ask.serialize(),
            "calculated_at": string_to_date(self.calculated_at),
        }
