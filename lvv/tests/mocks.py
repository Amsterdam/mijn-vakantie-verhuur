import json
import os

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')
FIXTURE_REGISTRATION_BSN_PATH = os.path.join(FIXTURE_PATH, 'registration_bsn.json')
FIXTURE_REGISTRATION_ITEM_PATH = os.path.join(FIXTURE_PATH, 'registration_item.json')


def get_fixture_registration_bsn():
    with open(FIXTURE_REGISTRATION_BSN_PATH) as fp:
        return fp.read()


class ResponseMock:
    status_code = 200

    def __init__(self, data):
        self.data = data

    def content(self):
        return self.data

    def json(self):
        return json.loads(self.data)


class RequestsMock:
    @staticmethod
    def get(url, headers):
        if url == "http://localhost/registrations/AAAAAAAAAAAAAAAAAAAA":
            with open(FIXTURE_REGISTRATION_ITEM_PATH) as fh:
                return ResponseMock(fh.read())
        else:
            raise Exception(f"No fixture found for url: {url}")

    @staticmethod
    def post(url, headers, data):
        if url == "http://localhost/registrations/bsn":
            if data == '"111222333"':
                with open(FIXTURE_REGISTRATION_BSN_PATH) as fh:
                    return ResponseMock(fh.read())

        raise Exception(f"No fixture found for url: {url} body: {data[0:500]}")
