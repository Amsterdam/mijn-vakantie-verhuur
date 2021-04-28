import logging
from pprint import pprint
from sys import argv

from lvv.api.lvv.lvv_connection import LvvConnection
from lvv.config import get_lvv_api_host, get_lvv_key

logging.basicConfig(level=logging.DEBUG)

bsn = argv[1]

connection = LvvConnection(get_lvv_api_host(), get_lvv_key())
data = connection.get_data(bsn)
pprint(data)
