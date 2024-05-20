from config.socket_base_class import BaseWebSocket
from services.buda.socket import BudaWebSocket
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch


class TestBudaSocket(IsolatedAsyncioTestCase):
    def test_instances_correctly(self):
        buda_socket_class = BudaWebSocket()
        self.assertIsInstance(buda_socket_class, BudaWebSocket)

    def test_parse_market_ids(self):
        buda_socket_class = BudaWebSocket()
        parsed_result = buda_socket_class._parse_market_ids(["btc-clp", "ETH-CLP"])
        expected = ["book@btcclp", "book@ethclp"]

        self.assertEqual(parsed_result, expected)

    @patch.object(BaseWebSocket, "listen")
    async def test_listen_to_books(self, mock_listen):
        buda_socket_class = BudaWebSocket()

        async def on_message(ws):
            pass

        parsed_market_ids = ["BTC-CLP", "ETH-CLP"]

        await buda_socket_class.listen_to_books(
            market_ids=parsed_market_ids, on_message=on_message
        )

        self.assertTrue(mock_listen.called)
        mock_listen.assert_called_once_with(
            channels=["book@btcclp", "book@ethclp"], on_message=on_message
        )
