from app.repositories.auth_repository import get_user_info
from app.core.hashed_pw_verify import verify_password

def get_user(user_id,password):
    result = get_user_info(user_id)

    # ID가 틀린 경우
    if result is None:
        return {
            "message" : "User information does not exist"
            ,"error-code" : "E002"
            ,"flag" : False
        }

    # 아이디가 맞은 경우
    # 입력받은 비밀번호와 저장된 비밀번호가 같은지 검증
    isflag = verify_password(result["hashed_password"],password)

    if isflag :
        return {
            "access_token": "eyJ...",
            "token_type": "bearer",
            "expires_in": 900,
            "flag" : True
        }
    else :
        return {
            "message" : "incorrect"
            ,"error-code" : "E002"
            ,"flag" : False
        }