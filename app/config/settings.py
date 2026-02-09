"""
애플리케이션 내부에서 쓸 env 변수 모음(직접 env 파일에 접근 x)
"""
import os

from dotenv import load_dotenv

load_dotenv()

# 서버 설정
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
RELOAD = bool(os.getenv("RELOAD", False))

# Database 설정
DATABASE_URL = os.getenv("DATABASE_URL")
DB_TYPE = os.getenv("DB_TYPE", "postgres").lower()

# JWT 설정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))

# Token 수명 설정
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Token Storage 설정
TOKEN_STORAGE = os.getenv("TOKEN_STORAGE", "memory").lower()  # memory, redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# 로깅 설정
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
