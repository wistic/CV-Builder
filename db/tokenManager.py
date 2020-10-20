import pymysql
import datetime

from utility import logger


def validate_token(token, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Password_hash` FROM `Credentials` WHERE `Student_id`=%s"
            cursor.execute(sql, (token,))
            result = cursor.fetchall()
    except pymysql.Error:
        logger.critical('Token Insertion Error')


def insert_token(token, connection):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        connection.commit()
    except pymysql.Error:
        logger.critical('Token Insertion Error')
