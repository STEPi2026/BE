import os
import unittest
from unittest.mock import patch

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_NAME", "stepi_test")
os.environ.setdefault("DB_USER", "stepi_test")
os.environ.setdefault("DB_PASSWORD", "not-a-real-password")
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-only-secret-key-that-is-longer-than-32-characters",
)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password, verify_password
from app.db.database import Base, get_db
from app.db.models.user import User
from app.main import app


class SignupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite+pysqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=cls.engine, tables=[User.__table__])
        cls.SessionLocal = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine, tables=[User.__table__])
        cls.engine.dispose()

    def setUp(self):
        self.db: Session = self.SessionLocal()

        def override_get_db():
            yield self.db

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.db.rollback()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def signup(self, **overrides):
        payload = {
            "email": "student@example.com",
            "password": "safe-password-123",
            "name": "STEPi Student",
        }
        payload.update(overrides)
        return self.client.post("/auth/signup", json=payload)

    def test_signup_creates_student_with_hashed_password(self):
        response = self.signup()

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["email"], "student@example.com")
        self.assertEqual(body["name"], "STEPi Student")
        self.assertEqual(body["role"], "STUDENT")
        self.assertNotIn("password", body)
        self.assertNotIn("password_hash", body)

        user = self.db.scalar(select(User).where(User.email == "student@example.com"))
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, "safe-password-123")
        self.assertTrue(verify_password("safe-password-123", user.password_hash))

    def test_duplicate_email_returns_conflict(self):
        self.assertEqual(self.signup().status_code, 201)

        response = self.signup(name="Another Student")

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "Email is already registered")

    def test_invalid_email_returns_validation_error(self):
        response = self.signup(email="not-an-email")

        self.assertEqual(response.status_code, 422)

    def test_short_password_returns_validation_error(self):
        response = self.signup(password="short")

        self.assertEqual(response.status_code, 422)

    def test_missing_required_field_returns_validation_error(self):
        response = self.client.post(
            "/auth/signup",
            json={"email": "student@example.com", "password": "safe-password-123"},
        )

        self.assertEqual(response.status_code, 422)

    def test_database_unique_conflict_rolls_back_and_returns_conflict(self):
        self.db.add(
            User(
                email="student@example.com",
                password_hash=hash_password("safe-password-123"),
                name="Existing Student",
                role="STUDENT",
            )
        )
        self.db.commit()

        with patch.object(self.db, "scalar", return_value=None):
            response = self.signup()

        self.assertEqual(response.status_code, 409)
        users = self.db.scalars(
            select(User).where(User.email == "student@example.com")
        ).all()
        self.assertEqual(len(users), 1)
