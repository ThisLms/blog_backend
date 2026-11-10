import os
import jwt
import datetime

from app.repositories.auth_repository import repository_confirm_user
from app.core.hashed_pw_verify import verify_password

def issue_access_token(user_info):
    now = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "sub" : str(user_info["user_id"]) # 유저 고유 아이디
        ,"type" : "access" # 토큰의 종류
        ,"iat" : now # 토큰 발급 시간
        ,"exp" : now + datetime.timedelta(minutes=15) # 토큰 만료 시간(15분 후)
    }
    access_token = jwt.encode(
        payload
        ,os.environ["TOKEN_KEY"]
        ,algorithm=os.environ["TOKEN_ALGORITHM"]
    )

    return access_token

def service_login(login_id,password):

    # 데이터 베이스 조회를 위해 리포지토리에 보냄
    user_info = repository_confirm_user(login_id)

    # ID가 틀려서 아무런 정보도 없는 경우
    if user_info is None:
        return {
            "message" : "Invalid ID or password"
            ,"error-code" : "E002"
            ,"flag" : False
        }

    # 아이디가 맞은 경우
    # 입력받은 비밀번호와 저장된 비밀번호가 같은지 검증
    is_password_valid = verify_password(user_info["hashed_password"],password)

    # 비밀번호가 일치하지 않는 경우
    if not is_password_valid :
        return {
            "message" : "Invalid ID or password"
            ,"error-code" : "E002"
            ,"flag" : False
        }

    # 모든 인증을 통과한 후에는 토큰 생성
    access_token = issue_access_token(user_info) # access_token

    # 로그인 성공 - 토큰 및 정보 반환 
    return {
        "message" : "Login Success"
        ,"access_token" : access_token
        ,"flag" : True
    }