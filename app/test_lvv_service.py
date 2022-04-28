from unittest import TestCase
from unittest.mock import patch

from app.lvv_service import LvvConnection
from app.fixtures.mocks import RequestsMock


class CleopatraConnectionTest(TestCase):
    TEST_BSN = "111222333"

    @patch("app.lvv_service.requests", RequestsMock)
    def test_get_registration_numbers(self):
        con = LvvConnection("http://localhost/", "key")
        reg_numbers = con._bsn_to_registration_numbers(self.TEST_BSN)
        self.assertEqual(reg_numbers, ["AAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBBBBBBBBBBB"])

    @patch("app.lvv_service.requests", RequestsMock)
    def test_get_data(self):
        con = LvvConnection("http://localhost/", "key")
        result = con.get_data(self.TEST_BSN)
        reg_numbers = [i["registrationNumber"] for i in result]
        self.assertEqual(reg_numbers, ["AAAA AAAA AAAA AAAA AAAA"])
