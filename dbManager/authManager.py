import pymysql

from utility import logger, hash_password, verify_password


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


def change_password(enrollment_no, current_password, new_password, confirm_new_password, connection):
    status = verify_login(enrollment_no, current_password, connection)
    if status == "Database inconsistency - Call Admin":
        return status
    elif status == "Password required" or status == "Invalid Enrollment Number or Password":
        return "Current password incorrect"
    elif new_password != confirm_new_password or new_password == '' or confirm_new_password == '':
        return "Given passwords aren't acceptable"
    elif new_password == current_password:
        return "New Password should be different than old one"
    elif status == "Login Success":
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE `Credentials` SET `Password_hash`=%s WHERE `Student_id`=%s"
                hashed_password = hash_password(new_password)
                cursor.execute(sql, (hashed_password, enrollment_no))
        except (pymysql.Error, AttributeError):
            logger.critical('Password Validation Error')
            return "Database inconsistency - Call Admin"
        else:
            status = "Password updated successfully"
            return status
