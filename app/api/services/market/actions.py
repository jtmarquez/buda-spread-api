import logging

from config.exceptions.database_error import DatabaseErrorException
from services.market.model import Market
from peewee import DatabaseError


class MarketActions:
    def find_one(pair_name: str) -> Market:
        try:
            market = Market.select().where(Market.pair_name == pair_name).limit(1).get()
        except Market.DoesNotExist:
            return
        except DatabaseError as e:
            logging.error(f"Failed to obtain market: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to obtain market: {e}")
            return

        return market

    @staticmethod
    def create(pair_name: str) -> Market:
        try:
            market = Market.create(pair_name=pair_name)
        except DatabaseError as e:
            raise DatabaseErrorException(message=f"Failed to create market: {e}")
        except Exception as e:
            raise DatabaseErrorException(message=f"Failed to create market: {e}")

        return market
