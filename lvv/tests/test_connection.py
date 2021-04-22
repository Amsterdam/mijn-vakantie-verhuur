from unittest import TestCase
from unittest.mock import patch

from lvv.api.lvv.lvv_connection import LvvConnection
from lvv.tests.mocks import RequestsMock


class CleopatraConnectionTest(TestCase):
    def setUp(self) -> None:
        pass

    @patch("lvv.api.lvv.lvv_connection.requests", RequestsMock)
    def test_get_data(self):
        con = LvvConnection("http://localhost", "key")
        con.get_data("123456789")


