import unittest
from unittest.mock import patch, Mock

from config.exceptions.database_error import DatabaseErrorException
from controllers.spread import SpreadController
from controllers.user_spread_alerts import UserSpreadAlertController
from services.market.actions import MarketActions
from services.market_ask.actions import MarketAskActions
from services.market_bid.actions import MarketBidActions
from controllers.market_tick import MarketTickController
from services.market_spread.actions import MarketSpreadActions
from services.market_tick.config.types import TickType
from services.user_spread.actions import UserSpreadActions


class TestMarketTickController(unittest.TestCase):
    @patch.object(MarketActions, "find_one")
    @patch.object(MarketActions, "create")
    @patch.object(MarketAskActions, "create")
    @patch.object(MarketBidActions, "create")
    def test_create_tick_without_market(
        self, mock_create_bid, mock_create_ask, mock_create_market, mock_find_market
    ):

        market_pair_id = "btcclp"
        tick_type = TickType.ASKS
        value = 100

        mock_find_market.return_value = None
        mock_create_market.return_value = Mock(serialize=Mock(return_value={"id": 1}))

        MarketTickController.create(market_pair_id, tick_type, value)

        mock_find_market.assert_called_once_with(pair_name=market_pair_id)
        mock_create_market.assert_called_once_with(pair_name=market_pair_id)
        mock_create_ask.assert_called_once_with(
            value=value, market_pair_key=market_pair_id
        )
        mock_create_bid.assert_not_called()

    @patch.object(MarketActions, "find_one")
    @patch.object(MarketActions, "create")
    @patch.object(MarketAskActions, "create")
    @patch.object(MarketBidActions, "create")
    def test_create_tick_with_market(
        self, mock_create_bid, mock_create_ask, mock_create_market, mock_find_market
    ):

        market_pair_id = "btcclp"
        tick_type = TickType.BIDS
        value = 100

        mock_find_market.return_value = Mock(serialize=Mock(return_value={"id": 1}))

        MarketTickController.create(market_pair_id, tick_type, value)

        mock_find_market.assert_called_once_with(pair_name=market_pair_id)
        mock_create_market.assert_not_called()
        mock_create_ask.assert_not_called()
        mock_create_bid.assert_called_once_with(
            value=value, market_pair_key=market_pair_id
        )

    @patch.object(MarketActions, "find_one")
    @patch.object(MarketActions, "create")
    @patch.object(MarketAskActions, "create")
    @patch.object(MarketBidActions, "create")
    def test_create_tick_with_invalid_tick_type(
        self, mock_create_bid, mock_create_ask, mock_create_market, mock_find_market
    ):

        market_pair_id = "btcclp"
        tick_type = "INVALID"
        value = 100

        mock_find_market.return_value = None
        mock_create_market.return_value = Mock(serialize=Mock(return_value={"id": 1}))

        with self.assertRaises(Exception) as context:
            MarketTickController.create(market_pair_id, tick_type, value)

        self.assertEqual(
            str(context.exception), f"Error: Invalid tick type: {tick_type}"
        )
        mock_find_market.assert_called_once_with(pair_name=market_pair_id)
        mock_create_market.assert_called_once_with(pair_name=market_pair_id)
        mock_create_ask.assert_not_called()
        mock_create_bid.assert_not_called()


class TestSpreadController(unittest.TestCase):
    @patch("utils.parse_market_id.parse_market_id")
    @patch.object(MarketBidActions, "find_all")
    @patch.object(MarketAskActions, "find_all")
    @patch.object(MarketSpreadActions, "get_market_spreads")
    def test_get_spreads_with_market_pair_id(
        self,
        mock_get_spreads,
        mock_find_all_asks,
        mock_find_all_bids,
        mock_parse_market_id,
    ):

        market_pair_id = "BTC-CLP"

        mock_parse_market_id.return_value = "BTC-CLP"
        mock_find_all_asks.return_value = [Mock()]
        mock_find_all_bids.return_value = [Mock()]
        mock_get_spreads.return_value = [Mock(serialize=Mock(return_value={"id": 1}))]

        spreads = SpreadController.get_spreads(market_pair_id)

        mock_find_all_asks.assert_called_once_with(
            market_id=market_pair_id, latest=True
        )
        mock_find_all_bids.assert_called_once_with(
            market_id=market_pair_id, latest=True
        )
        mock_get_spreads.assert_called_once_with(
            mock_find_all_bids.return_value, mock_find_all_asks.return_value
        )
        for serialized in mock_get_spreads.return_value:
            serialized.serialize.assert_called_once()
        self.assertEqual(spreads, [{"id": 1}])

    @patch("controllers.spread.parse_market_id")
    @patch.object(MarketBidActions, "find_all")
    @patch.object(MarketAskActions, "find_all")
    @patch.object(MarketSpreadActions, "get_market_spreads")
    def test_get_spreads_without_market_pair_id(
        self,
        mock_get_spreads,
        mock_find_all_asks,
        mock_find_all_bids,
        mock_parse_market_id,
    ):

        market_pair_id = None

        mock_parse_market_id.return_value = None
        mock_find_all_asks.return_value = [Mock()]
        mock_find_all_bids.return_value = [Mock()]
        mock_get_spreads.return_value = [Mock(serialize=Mock(return_value={"id": 1}))]

        spreads = SpreadController.get_spreads(market_pair_id)

        mock_parse_market_id.assert_not_called()
        mock_find_all_asks.assert_called_once_with(
            market_id=market_pair_id, latest=True
        )
        mock_find_all_bids.assert_called_once_with(
            market_id=market_pair_id, latest=True
        )
        mock_get_spreads.assert_called_once_with(
            mock_find_all_bids.return_value, mock_find_all_asks.return_value
        )
        for serialized in mock_get_spreads.return_value:
            serialized.serialize.assert_called_once()

        self.assertEqual(spreads, [{"id": 1}])


class TestUserSpreadAlertController(unittest.TestCase):
    @patch.object(UserSpreadActions, "get")
    @patch.object(MarketBidActions, "find_all")
    @patch.object(MarketAskActions, "find_all")
    @patch.object(MarketSpreadActions, "get_market_spreads")
    def test_get_user_spread_alerts(
        self, mock_get_spreads, mock_find_all_asks, mock_find_all_bids, mock_get
    ):

        spread_alert_id = 1

        mock_get.return_value = Mock(
            serialize=Mock(return_value={"id": 1}), market_id="btcclp"
        )
        mock_find_all_asks.return_value = [Mock()]
        mock_find_all_bids.return_value = [Mock()]
        mock_get_spreads.return_value = [Mock(serialize=Mock(return_value={"id": 1}))]

        user_spread_alerts = UserSpreadAlertController.get_user_spread_alerts(
            spread_alert_id
        )

        mock_get.assert_called_once_with(id=spread_alert_id)
        mock_find_all_asks.assert_called_once_with(
            market_id=mock_get.return_value.market_id, latest=True
        )
        mock_find_all_bids.assert_called_once_with(
            market_id=mock_get.return_value.market_id, latest=True
        )
        mock_get_spreads.assert_called_once_with(
            mock_find_all_bids.return_value, mock_find_all_asks.return_value
        )
        mock_get_spreads.return_value[0].serialize.assert_called_once()
        mock_get.return_value.serialize.assert_called_once()

        self.assertEqual(
            user_spread_alerts,
            {
                "saved_spread": mock_get.return_value.serialize.return_value,
                "current_spread": mock_get_spreads.return_value[
                    0
                ].serialize.return_value,
            },
        )

    @patch.object(UserSpreadActions, "create")
    def test_create_user_spread_alert(self, mock_create):

        market_id = "btcclp"
        spread = 100

        mock_create.return_value = Mock(serialize=Mock(return_value={"id": 1}))

        user_spread_alert = UserSpreadAlertController.create_user_spread_alert(
            market_id, spread
        )

        mock_create.assert_called_once_with(market_id=market_id, value=spread)
        mock_create.return_value.serialize.assert_called_once()

        self.assertEqual(
            user_spread_alert, mock_create.return_value.serialize.return_value
        )
