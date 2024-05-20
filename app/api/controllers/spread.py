from services.config.serializer_types import SerializedMarketSpread
from services.market_spread.actions import MarketSpreadActions
from utils.parse_market_id import parse_market_id
from services.market_ask.actions import MarketAskActions
from services.market_bid.actions import MarketBidActions
from config.base_classes.base_controller import BaseController


class SpreadController(BaseController):
    @staticmethod
    def get_spreads(market_pair_id: str = None) -> list[SerializedMarketSpread]:
        parsed_mkt_id = parse_market_id(market_pair_id) if market_pair_id else None

        bids = MarketBidActions.find_all(market_id=parsed_mkt_id, latest=True)
        asks = MarketAskActions.find_all(market_id=parsed_mkt_id, latest=True)

        market_spreads = MarketSpreadActions.get_market_spreads(bids, asks)

        spreads = [spread.serialize() for spread in market_spreads]

        return spreads
