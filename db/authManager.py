from utility import verify_password
import pymysql

from utility import logger


def verify_login(enrollment_no, password, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Password_hash` FROM `Credentials` WHERE `Student_id`=%s"
            cursor.execute(sql, (enrollment_no,))
            result = cursor.fetchall()
    except (pymysql.Error, AttributeError):
        logger.critical('Password Validation Error')
        return "Database inconsistency - Call Admin"

    if enrollment_no == '':
        return "Enrollment Number required"
    elif not enrollment_no.isdigit():
        return "Enrollment Number is a pure number."
    elif password == '':
        return "Password required"
    elif len(result) == 0:
        return "Invalid Enrollment Number or Password"
    elif len(result) > 1:
        return "Database inconsistency - Call Admin"
    else:
        stored_password = result[0]['Password_hash']
        if verify_password(stored_password, password):
            return "Login Success"
        else:
            return "Invalid Enrollment Number or Password"
