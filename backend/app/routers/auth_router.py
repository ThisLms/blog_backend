from fastapi import APIRouter,HTTPException

from app.schemas.login import LoginRequest
from app.services.auth_service import service_login

router = APIRouter()

@router.post("/login")
def router_login(data: LoginRequest):

    # 프론트 엔드에서 값을 받음
    login_id = data.login_id
    password = data.password

    # 받은 값을 서비스로 전송
    result = service_login(login_id,password)

    # 인증에 성공했을 때
    if result["flag"]:
        return {
            "access_token" : result["access_token"]
            ,"token_type" : "bearer"
            ,"expires_in" : 900 # 15 분을 초로 변환 
        }
    # 인증에 실패했을 때
    else:
        if result["error-code"] == "E002":
            raise HTTPException(
                status_code=401,
                detail="ID・パスワードが一致しないです。"
            )