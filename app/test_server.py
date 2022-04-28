import os
from unittest.mock import patch
from app.auth import FlaskServerTestCase

from app.server import app
from app.fixtures.mocks import RequestsMock


@patch.dict(os.environ, {"LVV_HOST": "http://localhost/"})
@patch("app.lvv_service.requests", RequestsMock)
class ServerTests(FlaskServerTestCase):

    app = app

    def test_status(self):
        response = self.client.get("/status/health")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["content"], "OK")

    def test_get(self):
        response = self.get_secure("/vakantie-verhuur/get")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json["content"],
            [
                {
                    "city": "Amsterdam",
                    "houseLetter": None,
                    "houseNumber": "1",
                    "houseNumberExtension": None,
                    "postalCode": "1012PN",
                    "registrationNumber": "AAAA AAAA AAAA AAAA AAAA",
                    "shortName": "Amstel",
                    "street": "Amstel",
                    "agreementDate": "2021-01-01T10:47:44.6107122",
                }
            ],
        )

    def test_no_token(self):
        response = self.client.get("/vakantie-verhuur/get")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, {"message": "Auth error occurred", "status": "ERROR"}
        )
