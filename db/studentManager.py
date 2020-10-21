import pymysql

from utility import logger


def get_student_data(student_id, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `Students` WHERE `Student_id`=%s"
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()
            if result is not None:
                return result
            else:
                return "Empty Set"
    except (pymysql.Error, AttributeError):
        logger.critical('Token Validation Error')
