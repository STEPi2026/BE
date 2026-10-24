from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router

app = FastAPI(
    title="P5 AI Tutor Backend",
    description="P5 적응형 AI Tutor Agent Backend API",
    version="0.1.0"
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "P5 AI Tutor Backend Server"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected"
    }
