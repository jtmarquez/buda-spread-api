from services.market_bid.model import MarketBid

import logging
from peewee import fn, DatabaseError


class MarketBidActions:
    @staticmethod
    def create(
        value: float,
        market_pair_key: str,
    ) -> MarketBid:
        try:
            bid = MarketBid.create(
                value=value,
                market_id=market_pair_key,
            )
        except DatabaseError as e:
            logging.error(f"Failed to create market bid: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to create market bid: {e}")
            return

        return bid

    @staticmethod
    def find_all(market_id: str = None, latest=False):
        try:
            query = MarketBid.select()

            if latest:
                query = query.group_by(MarketBid.market_id).having(
                    fn.MAX(MarketBid.created_at)
                )

            if market_id:
                query = query.where(MarketBid.market_id == market_id)

        except DatabaseError as e:
            logging.error(f"Failed to find market bids: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to find market bids: {e}")
            return

        return query
