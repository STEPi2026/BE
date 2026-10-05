from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


# MySQL 연결 엔진
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)


# DB 세션 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 앞으로 SQLAlchemy 모델들이 상속받을 기본 클래스
class Base(DeclarativeBase):
    pass


# FastAPI에서 DB를 사용할 때 호출할 함수
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()