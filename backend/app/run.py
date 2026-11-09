from fastapi import FastAPI
from app.routers.auth_router import router as auth_router

# app = FastAPI(...) 아래


app = FastAPI(
    title="blog for developer API",
    description=(
        "エンジニアが技術情報や開発に関する質問、"
        "日々の経験を共有するための掲示板APIです。"
    )
)

app.include_router(auth_router)

@app.get("/")
def test_fast_api():
    return {
        "message" : "connect API test"
    }