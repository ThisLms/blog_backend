import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv
 
# 로컬에서는 backend/.env를 읽음
# 서버에서는 Compose가 전달한 환경변수를 우선 사용
load_dotenv(
    Path(__file__).resolve().parents[2] / ".env",
    override=False,
)

def get_connect():
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )