from fastapi import APIRouter,HTTPException,Header

from app.schemas.post import PostRequest
from app.services.post_service import service_post_register
from app.services.auth_service import service_verify

router = APIRouter()

@router.post("", status_code=201)
def router_post_register(data: PostRequest,authorization : str | None = Header(default=None)):
    result = service_verify(authorization)

    if result["flag"] == False:
        if result["status"] == "expire": # refresh token 再発行
            raise HTTPException (
                status_code=401
                ,detail=result["status"]
            )
        if result["status"] == "invalid" : # ログイン画面に遷移する
            raise HTTPException (
                status_code=401
                ,detail=result["status"]
            )
        if result["status"] == "not" : # ログイン画面に遷移する
            raise HTTPException (
                status_code=401
                ,detail=result["status"]
            )

    # result["flag"]가true일 경우
    user_id = result["user_id"]

    # 실질적인 등록 절차
    result = service_post_register(data,user_id)

    if result["flag"] == False:
        if result["error_code"] == "E015":
            raise HTTPException (
                status_code=422
                ,detail="入力値の形式またはデータ型が不正である"
            )

    return result