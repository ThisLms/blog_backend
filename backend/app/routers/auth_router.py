from fastapi import APIRouter,HTTPException,Response,Cookie

from app.schemas.login import LoginRequest
from app.services.auth_service import service_login,service_logout

router = APIRouter()

@router.post("/login")
def router_login(data: LoginRequest, response: Response):

    # 프론트 엔드에서 값을 받음
    login_id = data.login_id
    password = data.password

    # 받은 값을 서비스로 전송
    result = service_login(login_id,password)

    # 인증에 성공했을 때
    if result["flag"]:
        # 리프레시 토큰은 프론트 HttpOnly에 저장
        response.set_cookie (
            key="refresh_token"
            ,value=result["refresh_token"]
            ,httponly=True
            ,secure=True
            ,samesite="lax"
            ,max_age=14 * 24 * 60 * 60
        )

        # 엑세스 토큰은 프론트 앤드 세션에 저장
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

# 프론트 앤드에서 자동으로 리프레시 토큰을 백엔드로 보냄
@router.post("/logout")
def router_logout(refresh_token: str | None = Cookie(default=None)):
    if refresh_token is not None:
        service_logout(refresh_token)

    # HttpOnly의 리프레시 코인 제거
    response = Response(status_code=204)

    response.delete_cookie(
        key="refresh_token"
        ,httponly=True
        ,secure=True
        ,samesite="lax"
    )

    return response