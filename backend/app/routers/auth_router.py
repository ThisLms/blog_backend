from fastapi import APIRouter,HTTPException

from app.schemas.login import LoginRequest
from app.services.auth_service import get_user

router = APIRouter(
    prefix="/auth"
    ,tags=["auth"]
)

@router.post("/login")
def get_login(data: LoginRequest):
    user_id = data.user_id
    password = data.password

    result = get_user(user_id,password)

    if result["flag"]:
        return result
    else:
        if result["error-code"] == "E002":
            raise HTTPException(
                status_code=401,
                detail="ID・パスワードが一致しない"
            )