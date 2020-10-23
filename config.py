import os

try:
    mysql_host = os.environ['MYSQL_HOST']
except KeyError:
    mysql_host = '127.0.0.1'
try:
    mysql_user = os.environ['MYSQL_USER']
except KeyError:
    mysql_user = 'root'
try:
    mysql_password = os.environ['MYSQL_PASSWORD']
except KeyError:
    mysql_password = 'password'
try:
    mysql_db = os.environ['MYSQL_DB']
except KeyError:
    mysql_db = 'cv_builder'
try:
    mysql_charset = os.environ['MYSQL_CHARSET']
except KeyError:
    mysql_charset = 'utf8mb4'

config = {
    'host': mysql_host,
    'user': mysql_user,
    'password': mysql_password,
    'db': mysql_db,
    'charset': mysql_charset
}
