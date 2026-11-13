from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_rouetr

app = FastAPI(
    title="blog for developer API",
    description=(
        "エンジニアが技術情報や開発に関する質問、"
        "日々の経験を共有するための掲示板APIです。"
    )
)

app.add_middleware(
    CORSMiddleware,
    # api.moonlog.dev와는 same origin이 아니기 때문에 아래의 allow_origins가 필요
    allow_origins=[
        "https://moonlog.dev",
        "https://www.moonlog.dev",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# rooter 추가
app.include_router(
    auth_router
    ,prefix="/auth"
    ,tags=["auth"]
    )

app.include_router(
    user_rouetr
    ,prefix="/users"
    ,tags=["user"]
)

@app.get("/")
def test_fast_api():
    return {
        "message" : "Success"
    }