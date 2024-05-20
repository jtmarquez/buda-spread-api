from services.user_spread.model import UserSpread
from services.market_ask.model import MarketAsk
from services.market_bid.model import MarketBid
from config.database import database

from services.market.model import Market


def initial_setup():
    models = [Market, MarketBid, MarketAsk, UserSpread]
    database.create_tables(models)


if __name__ == "__main__":
    initial_setup()
