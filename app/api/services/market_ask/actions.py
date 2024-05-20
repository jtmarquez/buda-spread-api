import logging
from peewee import fn, DatabaseError

from services.market_ask.model import MarketAsk


class MarketAskActions:
    @staticmethod
    def create(
        value: float,
        market_pair_key: str,
    ) -> MarketAsk:
        try:
            ask = MarketAsk.create(
                value=value,
                market_id=market_pair_key,
            )
        except DatabaseError as e:
            logging.error(f"Failed to create market ask: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to create market ask: {e}")
            return

        return ask

    @staticmethod
    def find_all(market_id: str = None, latest=False):
        try:
            query = MarketAsk.select()

            if latest:
                query = query.group_by(MarketAsk.market_id).having(
                    fn.MAX(MarketAsk.created_at)
                )

            if market_id:
                query = query.where(MarketAsk.market_id == market_id)
        except DatabaseError as e:
            logging.error(f"Failed to find market asks: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to find market asks: {e}")
            return

        return query
