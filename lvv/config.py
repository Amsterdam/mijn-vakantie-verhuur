import os
import os.path


BASE_PATH = os.path.abspath(os.path.dirname(__file__))


def get_sentry_dsn():
    return os.getenv('SENTRY_DSN', None)


def get_lvv_key():
    return os.getenv("LVV_KEY")


def get_lvv_api_host():
    return os.getenv("LVV_API_HOST")


# def get_key():
#     return os.getenv("FERNET_KEY")


def get_tma_certificate():
    tma_cert_location = os.getenv('TMA_CERTIFICATE')
    with open(tma_cert_location) as f:
        return f.read()
