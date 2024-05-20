import logging
from services.user_spread.model import UserSpread
from peewee import DatabaseError


class UserSpreadActions:
    @staticmethod
    def create(market_id: str, value: float) -> UserSpread:
        try:
            user_spread = UserSpread.create(
                market_id=market_id,
                value=value,
            )
        except DatabaseError as e:
            logging.error(f"Failed to create user spread: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to create user spread: {e}")
            return

        return user_spread

    @staticmethod
    def get(id: str) -> UserSpread:
        try:
            user_spreads = UserSpread.get_by_id(id)
        except UserSpread.DoesNotExist:
            logging.error(f"User spread with id {id} not found")
            return
        except DatabaseError as e:
            logging.error(f"Failed to get user spread: {e}")
            return
        except Exception as e:
            logging.error(f"Failed to get user spread: {e}")
            return

        return user_spreads
