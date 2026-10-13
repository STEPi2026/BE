import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "3306")
os.environ.setdefault("DB_NAME", "stepi_test")
os.environ.setdefault("DB_USER", "stepi_test")
os.environ.setdefault("DB_PASSWORD", "not-a-real-password")
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-that-is-longer-than-32-characters"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

import jwt
from pydantic import ValidationError

from app.core.config import Settings, settings
from app.core.security import (
    AuthenticationError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.main import app, health_check
from app.routers.auth import authentication_status


class SecurityTests(unittest.TestCase):
    def test_jwt_secret_has_no_default_value(self):
        required_database_settings = {
            "DB_HOST": "localhost",
            "DB_PORT": "3306",
            "DB_NAME": "stepi_test",
            "DB_USER": "stepi_test",
            "DB_PASSWORD": "not-a-real-password",
        }

        with patch.dict(os.environ, required_database_settings, clear=True):
            with self.assertRaises(ValidationError):
                Settings(_env_file=None)

    def test_password_hash_and_verification(self):
        password = "correct-horse-battery-staple"
        password_hash = hash_password(password)

        self.assertNotEqual(password, password_hash)
        self.assertTrue(verify_password(password, password_hash))
        self.assertFalse(verify_password("incorrect-password", password_hash))

    def test_access_token_creation_and_verification(self):
        token = create_access_token(subject=123)
        payload = decode_access_token(token)

        self.assertEqual(payload["sub"], "123")
        self.assertIn("iat", payload)
        self.assertIn("exp", payload)
        self.assertEqual(set(payload), {"sub", "iat", "exp"})

    def test_expired_access_token_is_rejected(self):
        token = create_access_token("123", expires_delta=timedelta(seconds=-1))

        with self.assertRaises(AuthenticationError) as context:
            decode_access_token(token)

        self.assertEqual(context.exception.detail, "Access token has expired")

    def test_access_token_with_wrong_signature_is_rejected(self):
        now = datetime.now(timezone.utc)
        token = jwt.encode(
            {"sub": "123", "iat": now, "exp": now + timedelta(minutes=1)},
            "a-different-secret-key-that-is-longer-than-32-characters",
            algorithm=settings.JWT_ALGORITHM,
        )

        with self.assertRaises(AuthenticationError) as context:
            decode_access_token(token)

        self.assertEqual(context.exception.detail, "Could not validate credentials")

    def test_auth_router_and_health_routes_are_registered(self):
        self.assertEqual(authentication_status().model_dump(), {"status": "ready"})
        self.assertEqual(health_check(), {"status": "ok"})
        self.assertIn("/auth/status", app.openapi()["paths"])


if __name__ == "__main__":
    unittest.main()
