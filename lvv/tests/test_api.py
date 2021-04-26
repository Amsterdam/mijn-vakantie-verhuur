from unittest.mock import patch

from tma_saml import FlaskServerTMATestCase
from tma_saml.for_tests.cert_and_key import server_crt

from lvv.server import app
from lvv.tests.mocks import RequestsMock


class HealthTest(FlaskServerTMATestCase):
    def setUp(self) -> None:
        self.client = self.get_tma_test_app(app)

    def test_health(self):
        response = self.client.get('/status/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"OK")


@patch("lvv.api.lvv.lvv_connection.requests", RequestsMock)
@patch("lvv.server.get_lvv_api_host", lambda: "http://localhost")
@patch("lvv.server.get_tma_certificate", lambda: server_crt)
class ApiTest(FlaskServerTMATestCase):
    TEST_BSN = "111222333"

    def setUp(self) -> None:
        self.client = self.get_tma_test_app(app)

    def test_get(self):
        SAML_HEADERS = self.add_digi_d_headers(self.TEST_BSN)

        response = self.client.get("/vakantieverhuur/get", headers=SAML_HEADERS)
        self.assertTrue(response)