import pytest
from fastapi import HTTPException
from backend.app.api.endpoints.auth import login

class DummyForm:
    def __init__(self, username="user@example.com", password="wrongpass"):
        self.username = username
        self.password = password
        self.scopes = []
        self.client_id = None
        self.client_secret = None

@pytest.mark.asyncio
async def test_login_wrong_password_raises_401(monkeypatch):
    # Mock authenticate_user to simulate wrong password (returns None)
    monkeypatch.setattr(
        "backend.app.api.endpoints.auth.authenticate_user",
        lambda db, username, password: None
    )
    # Mock create_access_token to ensure it's never called (fails test if it is)
    def _should_not_be_called(*args, **kwargs):  # pragma: no cover
        pytest.fail("create_access_token should not be called on authentication failure")
    monkeypatch.setattr(
        "backend.app.api.endpoints.auth.create_access_token",
        _should_not_be_called
    )

    form_data = DummyForm()
    with pytest.raises(HTTPException) as exc_info:
        await login(form_data=form_data, db=None)  # db is irrelevant due to mocking

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect email or password"

import pytest
from fastapi import HTTPException, status
from backend.app.api.endpoints.auth import login

@pytest.mark.asyncio
async def test_login_unknown_user_raises_401(monkeypatch):
    # Mock authenticate_user to simulate unknown user
    def mock_authenticate_user(db, username, password):
        return None
    monkeypatch.setattr(
        "backend.app.api.endpoints.auth.authenticate_user",
        mock_authenticate_user,
        raising=True,
    )

    # Mock create_access_token even though it shouldn't be called in this path
    monkeypatch.setattr(
        "backend.app.api.endpoints.auth.create_access_token",
        lambda *args, **kwargs: "fixed-token",
        raising=True,
    )

    # Prepare dummy inputs matching only used attributes
    dummy_db = object()
    dummy_form = type("Form", (), {"username": "unknown@example.com", "password": "wrongpass"})()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await login(dummy_form, dummy_db)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Incorrect email or password"

import types
import pytest
from app.api.endpoints.auth import login

@pytest.mark.asyncio
async def test_login_happy_path(monkeypatch):
    dummy_db = object()
    dummy_username = "user@example.com"
    dummy_password = "correct-password"
    dummy_token = "fixed-token"
    dummy_user = types.SimpleNamespace(email=dummy_username)

    # Mock authenticate_user to return a valid user
    def fake_authenticate_user(db, username, password):
        assert db is dummy_db
        assert username == dummy_username
        assert password == dummy_password
        return dummy_user

    monkeypatch.setattr("app.api.endpoints.auth.authenticate_user", fake_authenticate_user)

    # Mock create_access_token to return a predictable token
    monkeypatch.setattr("app.api.endpoints.auth.create_access_token",
                        lambda data, expires_delta: dummy_token)

    # Mock UserSchema.from_orm to return a simple dict representation
    monkeypatch.setattr("app.schemas.user.User", "from_orm",
                        classmethod(lambda cls, obj: {"email": obj.email}), raising=False)

    # Dummy form data object mimicking OAuth2PasswordRequestForm
    class DummyForm:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    form_data = DummyForm(dummy_username, dummy_password)

    # Call the login function
    result = await login(form_data=form_data, db=dummy_db)

    # Assertions
    assert result["access_token"] == dummy_token
    assert result["token_type"] == "bearer"
    assert result["user"] == {"email": dummy_username}

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from unittest.mock import patch, MagicMock
from app.api.endpoints.auth import login


@pytest.mark.asyncio
async def test_login_missing_password_raises_401():
    form_data = OAuth2PasswordRequestForm(
        username="user@example.com",
        password="",
        scope="",
        client_id=None,
        client_secret=None
    )
    dummy_db = MagicMock()

    with patch("app.api.endpoints.auth.authenticate_user", return_value=None) as mock_auth, \
         patch("app.api.endpoints.auth.create_access_token", return_value="fixed-token") as mock_token, \
         patch("app.db.database.get_db", return_value=dummy_db):
        with pytest.raises(HTTPException) as exc_info:
            await login(form_data=form_data, db=dummy_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Incorrect email or password"
        mock_auth.assert_called_once_with(dummy_db, form_data.username, form_data.password)
        mock_token.assert_not_called()

import types
import pytest
from app.api.endpoints.auth import login
from types import SimpleNamespace

@pytest.mark.asyncio
async def test_login_happy_path(monkeypatch):
    # Arrange
    test_email = "user@example.com"
    dummy_user = SimpleNamespace(email=test_email)

    # Mock database interaction and authentication
    monkeypatch.setattr(
        "app.api.endpoints.auth.authenticate_user",
        lambda db, username, password: dummy_user
    )

    # Mock token creation to return a predictable value
    fake_token = "fixed-token"
    monkeypatch.setattr(
        "app.api.endpoints.auth.create_access_token",
        lambda *args, **kwargs: fake_token
    )

    # Mock the database dependency provider
    monkeypatch.setattr("app.db.database.get_db", lambda: None)

    # Prepare minimal form data stub
    form_data = SimpleNamespace(username=test_email, password="irrelevant")

    # Act
    result = await login(form_data, db=None)

    # Assert
    assert result["access_token"] == fake_token
    assert result["token_type"] == "bearer"
    assert result["user"].email == test_email

import pytest
from types import SimpleNamespace
from datetime import timedelta
from app.api.endpoints import auth as auth_module  # Accurate import based on file paths

@pytest.mark.asyncio
async def test_login_generates_token_with_correct_expiration(monkeypatch):
    # Arrange
    user_email = "user@example.com"
    dummy_user = SimpleNamespace(email=user_email)
    dummy_token = "fixed-token"
    captured = {}

    # Mock dependencies
    monkeypatch.setattr(auth_module, "authenticate_user", lambda db, username, password: dummy_user)

    def fake_create_access_token(*, data, expires_delta):
        captured["data"] = data
        captured["expires_delta"] = expires_delta
        return dummy_token

    monkeypatch.setattr(auth_module, "create_access_token", fake_create_access_token)
    monkeypatch.setattr(auth_module.UserSchema, "from_orm", staticmethod(lambda u: {"email": u.email}))

    form_data = SimpleNamespace(username=user_email, password="any-password")

    # Act
    result = await auth_module.login(form_data=form_data, db=None)

    # Assert
    expected_delta = timedelta(minutes=auth_module.ACCESS_TOKEN_EXPIRE_MINUTES)
    assert captured["data"] == {"sub": user_email}
    assert captured["expires_delta"] == expected_delta
    assert result == {
        "access_token": dummy_token,
        "token_type": "bearer",
        "user": {"email": user_email},
    }