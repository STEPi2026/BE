import os
import unittest

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_NAME", "stepi_test")
os.environ.setdefault("DB_USER", "stepi_test")
os.environ.setdefault("DB_PASSWORD", "not-a-real-password")
os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-key-that-is-longer-than-32-characters")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import decode_access_token, hash_password
from app.db.database import Base, get_db
from app.db.models.user import User
from app.main import app


class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite+pysqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(bind=cls.engine, tables=[User.__table__])
        cls.SessionLocal = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine, tables=[User.__table__])
        cls.engine.dispose()

    def setUp(self):
        self.db: Session = self.SessionLocal()
        self.db.add(User(email="student@example.com", password_hash=hash_password("safe-password-123"), name="Student", role="STUDENT"))
        self.db.commit()
        app.dependency_overrides[get_db] = lambda: self.db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def test_login_returns_access_token(self):
        response = self.client.post("/auth/login", json={"email": "student@example.com", "password": "safe-password-123"})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["token_type"], "bearer")
        self.assertEqual(decode_access_token(body["access_token"])["sub"], "1")
        self.assertNotIn("password", body)
        self.assertNotIn("password_hash", body)

    def test_invalid_password_and_unknown_email_share_error(self):
        wrong = self.client.post("/auth/login", json={"email": "student@example.com", "password": "wrong"})
        unknown = self.client.post("/auth/login", json={"email": "unknown@example.com", "password": "safe-password-123"})
        self.assertEqual(wrong.status_code, 401)
        self.assertEqual(unknown.status_code, 401)
        self.assertEqual(wrong.json()["detail"], unknown.json()["detail"])

    def test_invalid_request_returns_validation_error(self):
        self.assertEqual(self.client.post("/auth/login", json={"email": "invalid", "password": "x"}).status_code, 422)
        self.assertEqual(self.client.post("/auth/login", json={"email": "student@example.com"}).status_code, 422)
