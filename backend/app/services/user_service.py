from datetime import date
from pymysql.err import IntegrityError

from app.core.hashed_pw_verify import hash_password
from app.core.check_form import check_form_email
from app.repositories.user_repository import repository_signup

def service_signup(data):
    email = data.email.strip()

    if not email or not check_form_email(email):
        return {
            "error_code" : "E016" # E016入力形式が不正
            ,"flag" : False
        }

    if data.gender not in ("",1,2):
        return {
            "error_code" : "E016" # E016入力形式が不正
            ,"flag" : False
        }

    gender = int(data.gender) if data.gender else None

    try:
        birthday = date.fromisocalendar(data.birthday) if data.birthday else None
    except ValueError:
        return {
            "error_code" : "E016" # E016入力形式が不正
            ,"flag" : False
        }
    
    user_info = {
        "login_id" : data.login_id,
        "hashed_password" : hash_password(data.password),
        "user_name" : data.user_name,
        "email" : email,
        "gender" : gender,
        "introduction" : data.introduction,
        "birthday" : birthday
    }

    try:
        repository_signup(user_info)
    except IntegrityError as exc:
        if exc.args[0] == 1062:
            return {
                "error_code" : "E014" # ID又はパスワードが重複される
                ,"flag" : False
            }
        raise

    return {
        "flag" : True
    }