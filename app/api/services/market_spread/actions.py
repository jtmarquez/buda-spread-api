from collections import defaultdict
from services.market_ask.model import MarketAsk
from services.market_bid.model import MarketBid
from services.market_spread.model import MarketSpread


class MarketSpreadActions:
    @staticmethod
    def get_market_spreads(
        bids: list[MarketBid], asks: list[MarketAsk]
    ) -> list[MarketSpread]:
        market_pairs = defaultdict(lambda: {"bid": None, "ask": None})

        for bid in bids:
            market_pairs[bid.market_id]["bid"] = bid

        for ask in asks:
            market_pairs[ask.market_id]["ask"] = ask

        spreads: list[MarketSpread] = [
            MarketSpreadActions.get_spread(pair["ask"], pair["bid"])
            for pair in market_pairs.values()
            if pair["bid"] and pair["ask"]
        ]

        return spreads

    @staticmethod
    def get_spread(ask: MarketAsk, bid: MarketBid) -> MarketSpread:
        if ask.market_id != bid.market_id:
            raise ValueError("Market IDs do not match")
        return MarketSpread(bid, ask)
