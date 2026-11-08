from fastapi import FastAPI

app = FastAPI(
    title="blog for developer API",
    description=(
        "エンジニアが技術情報や開発に関する質問、"
        "日々の経験を共有するための掲示板APIです。"
    )
)

@app.get("/")
def test_fast_api():
    return {
        "message" : "connect API test"
    }