import pymysql

from utility import logger


def get_student_data(student_id, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Students` WHERE `Student_id`=%s"
            cursor.execute(sql, (student_id,))
            return cursor.fetchone()
    except (pymysql.Error, AttributeError):
        logger.critical('Token Validation Error')
