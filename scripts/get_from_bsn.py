import logging
from pprint import pprint
from sys import argv

from app.config import get_lvv_api_host, get_lvv_key
from app.lvv_service import LvvConnection

bsn = argv[1]

connection = LvvConnection(get_lvv_api_host(), get_lvv_key())
data = connection.get_data(bsn)
pprint(data)
