# API 테스트를 위한 최소한의 설정
FROM python:3.12-slim

WORKDIR /app

# 패키지를 먼저 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# API 소스 코드 복사
COPY app ./app

# 관리자 계정 대신 일반 사용자로 실행
RUN useradd --create-home appuser
USER appuser

CMD ["python", "-m", "uvicorn", "app.run:app", "--host", "0.0.0.0", "--port", "8000"]