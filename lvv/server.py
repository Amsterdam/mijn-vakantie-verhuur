import logging

import sentry_sdk
from flask import Flask, request
from sentry_sdk.integrations.flask import FlaskIntegration
from tma_saml import get_digi_d_bsn, InvalidBSNException, SamlVerificationException, get_e_herkenning_attribs, \
    HR_KVK_NUMBER_KEY

from lvv.config import get_sentry_dsn, get_lvv_api_host, get_lvv_key, get_tma_certificate

logger = logging.getLogger(__name__)
app = Flask(__name__)

if get_sentry_dsn():  # pragma: no cover
    sentry_sdk.init(
        dsn=get_sentry_dsn(),
        integrations=[FlaskIntegration()],
        with_locals=False
    )


# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, time):
#             return obj.isoformat()
#         if isinstance(obj, date):
#             return obj.isoformat()
#
#         return JSONEncoder.default(self, obj)


# app.json_encoder = CustomJSONEncoder


def get_bsn_from_request(request):
    """
    Get the BSN based on a request, expecting a SAML token in the headers
    """
    # Load the TMA certificate
    tma_certificate = get_tma_certificate()

    # Decode the BSN from the request with the TMA certificate
    bsn = get_digi_d_bsn(request, tma_certificate)
    return bsn


def get_kvk_number_from_request(request):
    """
    Get the KVK number from the request headers.
    """
    # Load the TMA certificate
    tma_certificate = get_tma_certificate()

    # Decode the BSN from the request with the TMA certificate
    attribs = get_e_herkenning_attribs(request, tma_certificate)
    kvk = attribs[HR_KVK_NUMBER_KEY]
    return kvk


@app.route('/vakantieverhuur/get', methods=['GET'])
def get_lvv():
    kind = None
    identifier = None

    try:
        identifier = get_kvk_number_from_request(request)
        kind = 'kvk'
    except SamlVerificationException:
        return {'status': 'ERROR', 'message': 'Missing SAML token'}, 400
    except KeyError:
        # does not contain kvk number, might still contain BSN
        pass

    if kind == 'kvk':
        return {
            'status': "ERROR",
            'content': 'no KVK support'
        }, 400

    if not identifier:
        try:
            identifier = get_bsn_from_request(request)
            kind = 'bsn'
        except InvalidBSNException:
            return {"status": "ERROR", "message": "Invalid BSN"}, 400
        except SamlVerificationException as e:
            return {"status": "ERROR", "message": e.args[0]}, 400
        except Exception as e:
            logger.error("Error", type(e), str(e))
            return {"status": "ERROR", "message": "Unknown Error"}, 400

    # connection = LVVConnection(get_lvv_api_host(), get_lvv_key())
    return {
        'status': 'OK',
        'content': [],
    }


@app.route('/status/health')
def health_check():
    return 'OK'


if __name__ == '__main__':  # pragma: no cover
    app.run()
