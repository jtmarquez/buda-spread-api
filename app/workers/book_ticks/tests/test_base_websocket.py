from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, Mock, AsyncMock
from config.socket_base_class import BaseWebSocket


class TestBaseWebsocket(IsolatedAsyncioTestCase):
    def test_instances_correctly(self):
        base_uri = "ws://base_uri"
        base_websocket_class = BaseWebSocket(base_uri)
        self.assertIsInstance(base_websocket_class, BaseWebSocket)
        self.assertEqual(base_websocket_class._base_uri, base_uri)
        self.assertEqual(base_websocket_class._live_sockets, [])

    def test_parse_uri_channels(self):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        uri = "ws://localhost:8000"
        channels = ["btcclp", "ethclp"]
        parsed_uri = base_websocket_class._parse_uri_channels(uri, channels)
        expected = "ws://localhost:8000/sub?channel=btcclp,ethclp"
        self.assertEqual(parsed_uri, expected)

    def test_parse_uri_channels_without_channels(self):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        uri = "ws://localhost:8000"
        parsed_uri = base_websocket_class._parse_uri_channels(uri)
        self.assertEqual(parsed_uri, uri)

    @patch.object(BaseWebSocket, "_on_message")
    @patch("websockets.connect")
    async def test_listen(self, mock_connect, mock_on_message):
        base_websocket_class = BaseWebSocket("ws://base_uri")

        async def on_message(ws):
            pass

        uri = "ws://localhost:8000"
        channels = ["btcclp", "ethclp"]

        await base_websocket_class.listen(
            on_message=on_message, uri=uri, channels=channels
        )

        mock_connect.assert_called_once_with(
            "ws://localhost:8000/sub?channel=btcclp,ethclp", ping_interval=None
        )
        arg_to_assert = mock_on_message.call_args_list[0][0][1]
        self.assertEqual(arg_to_assert, on_message)


    @patch("websockets.connect", new_callable=AsyncMock)
    async def test_get_live_socket(self, mock_connect):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        uri = "ws://localhost:8000"

        live_socket = await base_websocket_class.get_live_socket(uri)
        self.assertEqual(base_websocket_class._live_sockets, [live_socket])
        self.assertEqual(live_socket, mock_connect.return_value)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_once_with(uri)

    @patch("websockets.connect")
    async def test_send_message(self, mock_connect):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        uri = "ws://localhost:8000"
        message = "message"

        await base_websocket_class.send_message(message, uri)
        self.assertTrue(mock_connect.called)
        mock_connect.assert_called_once_with(uri)

    @patch("websockets.connect")
    async def test_send_message_with_existent_connection(self, mock_connect):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        message = "message"
        existent_connection = AsyncMock()

        await base_websocket_class.send_message(
            message, existent_connection=existent_connection
        )
        self.assertFalse(mock_connect.called)
        existent_connection.send.assert_called_once_with(message)
    
    @patch("websockets.connect")
    async def test_send_message_without_uri(self, mock_connect):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        message = "message"
        mock_connect.return_value = AsyncMock()
        await base_websocket_class.send_message(message)
        mock_connect.assert_called_once_with("ws://base_uri")

    async def test_close_existent_sockets(self):
        base_websocket_class = BaseWebSocket("ws://base_uri")
        live_socket = AsyncMock()
        base_websocket_class._live_sockets.append(live_socket)

        await base_websocket_class.close_existent_sockets()
        live_socket.close.assert_called_once()
        self.assertListEqual(base_websocket_class._live_sockets, [])