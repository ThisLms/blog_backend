import os
import jwt
import hashlib

# このファイルはトークンの有効・無効などを検証するための機能のみ
def verify_token(token : str, expected_type : str):
    try:
        # トークンデコーダー又は検証
        payload = jwt.decode(
            token
            ,os.environ["TOKEN_KEY"]
            ,algorithms=os.environ["TOKEN_ALGORITHM"]
        )

        # トークンの種類や偽造検証
        ## トークンの種類の検証
        if payload.get("type") != expected_type:
            return {
                "error_code" : "E003"
                ,"message" : "Invalid Token Type"
                ,"status" : "invalid"
                ,"flag" : False
            }

        return {
            "message" : "verification Success"
            ,"flag" : True
        }
    except jwt.ExpiredSignatureError:
        return {
            "error_code" : "E003"
            ,"message" : "Token Expire"
            ,"status" : "expire"
            ,"flag" : False
        }
    except jwt.InvalidTokenError:
        return {
            "error_code" : "E003"
            ,"message" : "Not Valid"
            ,"status" : "invalid"
            ,"flag" : False
        }
    