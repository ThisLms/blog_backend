from fastapi import APIRouter,HTTPException


from app.schemas.signup import SignupRequest
from app.services.user_service import service_signup

router = APIRouter()

@router.post("/")
def router_join_member(data: SignupRequest):
    result = service_signup(data)

    if result["flag"]:
        return {
            "message" : "会員登録に成功しました"
        }

    if result["error_code"] == "E016":
        raise HTTPException (
            status_code=422
            ,detail="正しい値を入力してください。"
        )

    if result["error_code"] == 'E014':
        raise HTTPException (
            status_code=409
            ,detail="ログインIDまたはメールアドレスは既に使用されています。",
        )

    raise HTTPException (
        status_code=500
        ,detail="会員登録に失敗しました。"
    )