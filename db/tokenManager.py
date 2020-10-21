import pymysql
import datetime

from utility import logger


def insert_token(token, student_id, connection):
    now = datetime.datetime.now()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `User_Tokens` (`Session_hash`, `Student_id`, `CreatedAt`) VALUES (%s, %s, %s); "
            cursor.execute(sql, (token, student_id, now.strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
    except pymysql.Error:
        logger.critical('Token Insertion Error')


def remove_token(token, connection):
    student_id = get_student_id(token, connection)
    if student_id != -1:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `User_Tokens` WHERE `Session_hash`=%s"
                cursor.execute(sql, (token,))
            connection.commit()
        except (pymysql.Error, AttributeError):
            logger.critical('Token Removal Error')


def get_student_id(token, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Student_id` FROM `User_Tokens` WHERE `Session_hash`=%s"
            cursor.execute(sql, (token,))
            result = cursor.fetchone()
            if result is not None:
                student_id = result['Student_id']
            else:
                student_id = -1
        return student_id
    except (pymysql.Error, AttributeError):
        logger.critical('Token Validation Error')
