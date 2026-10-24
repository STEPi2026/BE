import os
import unittest
os.environ.setdefault("DB_HOST", "localhost"); os.environ.setdefault("DB_PORT", "3306"); os.environ.setdefault("DB_NAME", "stepi_test"); os.environ.setdefault("DB_USER", "stepi_test"); os.environ.setdefault("DB_PASSWORD", "x"); os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-key-that-is-longer-than-32-characters")
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.security import hash_password
from app.db.database import Base, get_db
from app.db.models.user import User
from app.main import app

class EmailCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine=create_engine("sqlite+pysqlite://", connect_args={"check_same_thread":False}, poolclass=StaticPool); Base.metadata.create_all(bind=cls.engine, tables=[User.__table__]); cls.Session=sessionmaker(bind=cls.engine)
    def setUp(self):
        self.db=self.Session(); self.db.add(User(email="used@example.com", password_hash=hash_password("safe-password-123"), name="Student", role="STUDENT")); self.db.commit(); app.dependency_overrides[get_db]=lambda:self.db; self.client=TestClient(app)
    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine, tables=[User.__table__]); cls.engine.dispose()
    def tearDown(self):
        app.dependency_overrides.clear(); self.db.query(User).delete(); self.db.commit(); self.db.close()
    def test_availability(self):
        self.assertTrue(self.client.get("/auth/check-email",params={"email":"new@example.com"}).json()["available"]); self.assertFalse(self.client.get("/auth/check-email",params={"email":"used@example.com"}).json()["available"])
    def test_invalid_email(self):
        self.assertEqual(self.client.get("/auth/check-email",params={"email":"invalid"}).status_code,422)
