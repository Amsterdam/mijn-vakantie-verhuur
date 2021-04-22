import logging

import requests

logger = logging.getLogger(__name__)


class LvvConnection:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def _get(self, url):
        headers = {
            "X-Api-Key": self.api_key
        }
        response = requests.get(url, headers=headers)

        logger.debug(url)
        logger.debug(response.status_code)
        logger.debug(response.content)
        return response

    def _transform(self, data):
        return data

    def _bsn_to_registration_numbers(self, bsn):
        url = f'{self.api_url}/ext/api/Registrations/bsn/{bsn}'
        response = self._get(url)
        return [r['registrationNumber'] for r in response.json()]

    def _get_registrations(self, reg_numbers):
        for reg_num in reg_numbers:
            url = f"{self.api_url}/ext/api/Registrations/{reg_num}"
            response = self._get(url)
            data = response.json()
            print("data", data)


    def get_data(self, bsn):
        registration_numbers = self._bsn_to_registration_numbers(bsn)
        registrations = self._get_registrations(registration_numbers)


