import os
import unittest

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_NAME", "stepi_test")
os.environ.setdefault("DB_USER", "stepi_test")
os.environ.setdefault("DB_PASSWORD", "not-a-real-password")
os.environ.setdefault(
    "JWT_SECRET_KEY", "test-only-secret-key-that-is-longer-than-32-characters"
)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token, hash_password
from app.db.database import Base, get_db
from app.db.models.user import User
from app.main import app


class CurrentUserTests(unittest.TestCase):
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
        self.user = User(
            email="student@example.com",
            password_hash=hash_password("safe-password-123"),
            name="Student",
            role="STUDENT",
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

        def override_get_db():
            yield self.db

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def test_returns_current_user_without_credentials(self):
        token = create_access_token(subject=self.user.id)

        response = self.client.get(
            "/users/me", headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.user.id,
                "email": "student@example.com",
                "name": "Student",
                "role": "STUDENT",
            },
        )
        self.assertNotIn("password", response.json())
        self.assertNotIn("password_hash", response.json())

    def test_rejects_missing_or_invalid_token(self):
        missing = self.client.get("/users/me")
        invalid = self.client.get(
            "/users/me", headers={"Authorization": "Bearer invalid-token"}
        )

        self.assertEqual(missing.status_code, 401)
        self.assertEqual(invalid.status_code, 401)
        self.assertEqual(missing.headers["www-authenticate"], "Bearer")

    def test_rejects_token_for_deleted_user(self):
        token = create_access_token(subject=self.user.id)
        self.db.delete(self.user)
        self.db.commit()

        response = self.client.get(
            "/users/me", headers={"Authorization": f"Bearer {token}"}
        )

        self.assertEqual(response.status_code, 401)
