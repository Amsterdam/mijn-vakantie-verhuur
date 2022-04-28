import json
import logging

import requests


class LvvConnection:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def _get(self, url):
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, headers=headers)

        logging.debug(url)
        logging.debug(response.status_code)
        logging.debug(response.content)
        return response

    def _post(self, url, body):
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=body)

        logging.debug(url)
        logging.debug(response.status_code)
        logging.debug(response.content)
        return response

    def _extract_fields(self, source_data, target, fields):
        for f in fields:
            target[f["name"]] = source_data[f["name"]]

    def _transform(self, data):
        """Transform a single registration to the frontend format."""
        fields = [{"name": "registrationNumber"}, {"name": "agreementDate"}]
        house_fields = [
            {"name": "street"},
            {"name": "houseNumber"},
            {"name": "houseLetter"},
            {"name": "houseNumberExtension"},
            {"name": "postalCode"},
            {"name": "city"},
            {"name": "shortName"},
        ]

        formatted_data = {}
        self._extract_fields(data, formatted_data, fields)
        self._extract_fields(data["rentalHouse"], formatted_data, house_fields)

        return formatted_data

    def _bsn_to_registration_numbers(self, bsn):
        url = f"{self.api_url}registrations/bsn"
        body = json.dumps(bsn)
        response = self._post(url, body)
        return [r["registrationNumber"].replace(" ", "") for r in response.json()]

    def _get_registrations(self, reg_numbers):
        registrations = []
        for reg_num in reg_numbers:
            url = f"{self.api_url}registrations/{reg_num}"
            response = self._get(url)
            data = response.json()
            registration = self._transform(data)
            if registration["city"].lower() == "amsterdam":
                registrations.append(registration)
        return registrations

    def get_data(self, bsn):
        registration_numbers = self._bsn_to_registration_numbers(bsn)
        registrations = self._get_registrations(registration_numbers)
        return registrations
