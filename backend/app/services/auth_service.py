import os
import jwt
import datetime
import hashlib
import secrets
import uuid

from app.repositories.auth_repository import repository_confirm_user,repository_insert_refresh_token,repository_delete_refresh_token
from app.core.hashed_pw_verify import verify_password
from app.core.hash_token import hash_refresh_token

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

def issue_refresh_token(user_info):
    now = datetime.datetime.now(datetime.timezone.utc)

    refresh_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        refresh_token.encode("utf-8")
    ).hexdigest()

    # 리프레시 토큰은 2주간 보관
    expires_at = (
        now + datetime.timedelta(days=14)
    )

    token = {
        "user_id" : user_info["user_id"]
        ,"token_hash" : token_hash
        ,"family_id" : str(uuid.uuid4())
        ,"expires_at" : expires_at.replace(tzinfo=None)
    }

    # 데이터 베이스에 저장
    repository_insert_refresh_token(token)
    return refresh_token

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
    ## 1. access token
    access_token = issue_access_token(user_info) # access_token
    ## 2. refresh token
    refresh_token = issue_refresh_token(user_info) # refresh_token

    # 로그인 성공 - 토큰 및 정보 반환 
    return {
        "message" : "Login Success"
        ,"access_token" : access_token
        ,"refresh_token" : refresh_token
        ,"flag" : True
    }

def service_logout(refresh_token):
    token_hash = hash_refresh_token(refresh_token)
    repository_delete_refresh_token(token_hash)