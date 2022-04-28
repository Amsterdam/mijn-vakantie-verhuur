import logging

import sentry_sdk
from flask import Flask, request
from requests import HTTPError
from sentry_sdk.integrations.flask import FlaskIntegration

from app import auth
from app.config import (
    IS_DEV,
    SENTRY_DSN,
    CustomJSONEncoder,
    get_lvv_api_host,
    get_lvv_key,
)
from app.helpers import error_response_json, success_response_json, validate_openapi
from app.lvv_service import LvvConnection

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

if SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=SENTRY_DSN, integrations=[FlaskIntegration()], with_locals=False
    )


@app.route("/vakantie-verhuur/get", methods=["GET"])
@auth.login_required
@validate_openapi
def get_lvv():
    user = auth.get_current_user()
    lvv_data = LvvConnection(get_lvv_api_host(), get_lvv_key()).get_data(user["id"])
    return success_response_json(lvv_data)


@app.route("/status/health")
def health_check():
    return success_response_json("OK")


@app.errorhandler(Exception)
def handle_error(error):

    error_message_original = f"{type(error)}:{str(error)}"

    msg_auth_exception = "Auth error occurred"
    msg_request_http_error = "Request error occurred"
    msg_server_error = "Server error occurred"

    logging.exception(error, extra={"error_message_original": error_message_original})

    if IS_DEV:  # pragma: no cover
        msg_auth_exception = error_message_original
        msg_request_http_error = error_message_original
        msg_server_error = error_message_original

    if isinstance(error, HTTPError):
        return error_response_json(
            msg_request_http_error,
            error.response.status_code,
        )
    elif auth.is_auth_exception(error):
        return error_response_json(msg_auth_exception, 401)

    return error_response_json(msg_server_error, 500)


if __name__ == "__main__":  # pragma: no cover
    app.run()
