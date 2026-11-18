import os
import jwt

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

        try:
            user_id = int(payload["sub"])
        except (KeyError, TypeError, ValueError):
            return {
                "error_code": "E003"
                ,"status": "invalid"
                ,"flag": False
            }

        return {
            "message" : "verification Success"
            ,"user_id": user_id
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
    