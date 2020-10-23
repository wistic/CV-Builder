import pymysql

from utility import *


def verify_login(student_id, password, connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `Password_hash` FROM `Credentials` WHERE `Student_id`=%s"
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()
    except (pymysql.Error, AttributeError):
        return Status.ERROR, "Database inconsistency"

    if result is None:
        return Status.FAILURE, "Invalid Student ID or Password"
    else:
        stored_password = result['Password_hash']
        if verify_password(stored_password, password):
            return Status.SUCCESS, "Login Successful"
        else:
            return Status.FAILURE, "Invalid Student ID or Password"


def change_password(student_id, current_password, new_password, confirm_new_password, connection):
    status_code, description = verify_login(student_id, current_password, connection)
    if status_code is Status.ERROR:
        return status_code, description
    elif status_code is Status.FAILURE:
        return status_code, "Current password incorrect"
    elif new_password != confirm_new_password:
        return Status.FAILURE, "Given passwords don't match"
    elif new_password == current_password:
        return Status.FAILURE, "New Password should be different than old one"
    elif status_code is Status.SUCCESS:
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `Credentials` SET `Password_hash`=%s WHERE `Student_id`=%s"
                hashed_password = hash_password(new_password)
                cursor.execute(sql, (hashed_password, student_id))
                description = "Password updated successfully"
                return status_code, description
        except (pymysql.Error, AttributeError):
            logger.critical('Password Validation Error')
            return Status.ERROR, "Database inconsistency"
