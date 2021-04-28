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
        """ Transform a single registration to the frontend format. """
        return data

    def _bsn_to_registration_numbers(self, bsn):
        url = f'{self.api_url}Registrations/bsn/{bsn}'
        response = self._get(url)
        return [r['registrationNumber'] for r in response.json()]

    def _get_registrations(self, reg_numbers):
        registrations = []
        for reg_num in reg_numbers:
            url = f"{self.api_url}Registrations/{reg_num}"
            response = self._get(url)
            data = response.json()
            registrations.append(self._transform(data))
        return registrations

    def get_data(self, bsn):
        registration_numbers = self._bsn_to_registration_numbers(bsn)
        registrations = self._get_registrations(registration_numbers)
        return registrations
