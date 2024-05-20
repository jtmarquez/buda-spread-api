from config.exceptions.invalid_tick_type import InvalidMarketTickType
from services.market_ask.actions import MarketAskActions
from services.market_bid.actions import MarketBidActions
from config.base_classes.base_controller import BaseController
from services.market.actions import MarketActions
from services.market_tick.config.types import TickType


class MarketTickController(BaseController):
    @staticmethod
    def create(market_pair_id: str, tick_type: TickType, value: float):
        market = MarketActions.find_one(pair_name=market_pair_id)
        if not market:
            market = MarketActions.create(pair_name=market_pair_id)
            
        if tick_type == TickType.ASKS:
            tick = MarketAskActions.create(value=value, market_pair_key=market_pair_id)
        elif tick_type == TickType.BIDS:
            tick = MarketBidActions.create(value=value, market_pair_key=market_pair_id)
        else:
            raise InvalidMarketTickType(f"Error: Invalid tick type: {tick_type}")

        return tick.serialize()
