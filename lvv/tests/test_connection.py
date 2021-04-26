from unittest import TestCase
from unittest.mock import patch

from lvv.api.lvv.lvv_connection import LvvConnection
from lvv.tests.mocks import RequestsMock


class CleopatraConnectionTest(TestCase):
    TEST_BSN = "111222333"

    @patch("lvv.api.lvv.lvv_connection.requests", RequestsMock)
    def test_get_data(self):
        con = LvvConnection("http://localhost", "key")
        result = con.get_data(self.TEST_BSN)
        reg_numbers = [i['registrationNumber'] for i in result]
        self.assertEqual(reg_numbers, ['AAAA AAAA AAAA AAAA AAAA'])

    # @patch("lvv.api.lvv.lvv_connection.requests", RequestsMock)
    # def test_log_levels(self):
    #     con = LvvConnection("http://localhost", "key")
    #     print(">>>", con.get_data(self.TEST_BSN))
