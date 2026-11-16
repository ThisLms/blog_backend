import os
import jwt
import datetime
import hashlib
import secrets
import uuid

from app.repositories.auth_repository import repository_confirm_user,repository_insert_refresh_token,repository_delete_refresh_token,transaction,get_refresh_token_info,revoke_refresh_token_family,get_user_info_for_reissue_token,mark_refresh_token_use
from app.core.hashed_pw_verify import verify_password
from app.core.hash_token import hash_refresh_token
from app.core.core_vreify_token import verify_token
from app.config.exceptions import InvalidRefreshToken

def issue_access_token(user_info):
    now = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "sub" : str(user_info["user_id"]) # 유저 고유 아이디
        ,"type" : "access" # 토큰의 종류
        ,"iat" : now # 토큰 발급 시간
        ,"exp" : now + datetime.timedelta(minutes=1) # 토큰 만료 시간(15분 후)
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
        ,"user_info" : {
            "user_name" : user_info["user_name"]
            ,"authority_name" : user_info["authority_name"]
        }
        ,"flag" : True
    }

def service_logout(refresh_token):
    # refresh tokenをハッシュしてfamail_idをもとにrefresh token 削除

    with transaction() as conn:
        token_hash = hash_refresh_token(refresh_token)
        token_info = get_refresh_token_info(conn,token_hash)
        if token_info is not None:
            repository_delete_refresh_token(token_info["family_id"],conn=conn)

def service_verify(authorization):
    # JavaScriptで確認したが、念のためトークンの有無をもう一度確認する
    if not authorization:
        return {
            "error_code" : "E003" # アクセストークが存在しない、または無効
            ,"status" : "not"
            ,"flag" : False
        }
    # トークンがある場合、有効かどうかを確認する

    ## authorizationを認証方法とトークンに分ける
    token = authorization.split()

    ## 送信されたトークンの形式が異なる場合
    ## トークンのみ送信されたり、Bearer認証方法ではない場合エラーを返す.
    if len(token) != 2 or token[0].lower() != "bearer":
        return {
            "error_code" : "E003"
            ,"status" : "invalid"
            ,"flag" : False
        }

    ## Accessトークン検証
    result = verify_token(token[1],"access")

    return result

def service_refresh_token(refresh_token):
    # refresh tokenがない場合
    if not refresh_token:
        return {
            "error_code" : "E003"
            ,"status" : "not"
            ,"flag" : False
        }

    # 1. refresh tokenをSHA-256にハッシュ
    token_hash = hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()
    
    reuse_detected = False
    result = None

    with transaction() as conn:
        # 2. DBからtoken_hashで照会
        token_info = get_refresh_token_info(conn,token_hash)

        # 3. 期間切れ、使用済み、廃棄状況確認
        ## 存在しないトークン
        if token_info is None:
            raise InvalidRefreshToken("refresh token情報が確認できませんでした。")

        ## 廃棄されたトークン
        if token_info["revoked_at"] is not None:
            raise InvalidRefreshToken("廃棄されたトークンです。")

        ## 使用済みのトークン
        if token_info["used_at"] is not None:
            ## 該当するトークンを破棄する。
            revoke_refresh_token_family(conn,token_info["family_id"])

            reuse_detected = True
        else:
            now = datetime.datetime.now(datetime.timezone.utc)

            refresh_expires_at = token_info["expires_at"].replace(
                tzinfo=datetime.timezone.utc
            )

            ## トークンの期間切れ
            if now >= refresh_expires_at:
                raise InvalidRefreshToken("期間切れのトークンです")

            ## トークンが期間切れではない場合、新しいトークンを発行する
            # 4. トークンに紐づいているuser_idをもとに最新の情報を取得する
            user_info = get_user_info_for_reissue_token(conn,token_info["user_id"])

            if user_info is None:
                raise InvalidRefreshToken("ユーザを見つかりませんでした。")

            # 5. 既存のトークンを使用済みかつ新しいrefresh tokrnを格納する
            ## family_idとexpires_atは既存の値で設定する

            new_refresh_token  = secrets.token_urlsafe(32)
            new_token_hash = hashlib.sha256(new_refresh_token.encode("utf-8")).hexdigest()
            
            token = {
                "user_id" : token_info["user_id"],
                "token_hash" : new_token_hash,
                "family_id" : token_info["family_id"],
                "expires_at" : token_info["expires_at"]
            }

            mark_refresh_token_use(conn,token_info["id"]) # 既存のトークン使用済みにする
            repository_insert_refresh_token(token,conn=conn) # 新しいrefresh token生成

            user_info["exp"] =  min(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
                                ,refresh_expires_at)

            access_token = issue_access_token(user_info)

            result = {
                "access_token": access_token
                ,"refresh_token": new_refresh_token
                ,"user_info" : {
                    "user_name" : user_info["user_name"]
                    ,"authority_name" : user_info["authority_name"]
                }
                ,"expires_at": token_info["expires_at"]
                ,"flag" : True
            }
    if reuse_detected:
        raise InvalidRefreshToken("使用済みのトークンです")

    return result