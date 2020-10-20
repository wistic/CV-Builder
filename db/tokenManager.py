import pymysql

from utility import logger


def validate_token(token, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Password_hash` FROM `Credentials` WHERE `Student_id`=%s"
            cursor.execute(sql, (token,))
            result = cursor.fetchall()
    except pymysql.Error:
        logger.critical('Database Error')
