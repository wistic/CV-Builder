import pymysql
from utility import logger
from config import config
from dbManager import remove_all_tokens

try:
    connection = pymysql.connect(**config,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True,
                                 connect_timeout=100)
    remove_all_tokens(connection)
except pymysql.Error:
    logger.critical('Unable to connect to the database.')
    connection = ''
