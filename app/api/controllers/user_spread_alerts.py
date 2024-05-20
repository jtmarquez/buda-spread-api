from config.exceptions.not_found import NotFoundException
from config.base_classes.base_controller import BaseController
from config.http.status_codes import StatusCodes
from serializers.exception_serializer import ExceptionSerializer
from services.market_ask.actions import MarketAskActions
from services.market_bid.actions import MarketBidActions
from services.market_spread.actions import MarketSpreadActions
from services.user_spread.actions import UserSpreadActions


class UserSpreadAlertController(BaseController):
    @staticmethod
    def get_user_spread_alerts(spread_alert_id: str):
        user_spread_alerts = UserSpreadActions.get(id=spread_alert_id)

        if not user_spread_alerts:
            raise NotFoundException(
                message=f"User spread alert with id {spread_alert_id} not found",
                status_code=StatusCodes.NOT_FOUND,
            )

        current_bids = MarketBidActions.find_all(
            market_id=user_spread_alerts.market_id, latest=True
        )
        current_asks = MarketAskActions.find_all(
            market_id=user_spread_alerts.market_id, latest=True
        )

        spreads = MarketSpreadActions.get_market_spreads(current_bids, current_asks)

        current_spread_diff = spreads[0] if spreads else None

        return {
            "saved_spread": user_spread_alerts.serialize(),
            "current_spread": (
                current_spread_diff.serialize() if current_spread_diff else None
            ),
        }

    @staticmethod
    def create_user_spread_alert(market_id: str, spread: float):
        user_spread_alert = UserSpreadActions.create(market_id=market_id, value=spread)

        return user_spread_alert.serialize()
