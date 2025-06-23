import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock, patch
from auth import create_jwt_token
from routes import register, login, update_profile
from schemas import UserCreate, UserAuth, UserUpdate
from models import User


def test_register_user_success():
    db = MagicMock()
    db.query().filter().first.return_value = None

    user_data = UserCreate(username="testuser", email="test@example.com", password="Passw0rd!")
    result_user = User(id=1, username="testuser", email="test@example.com", hashed_password="hashed")

    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock(side_effect=lambda x: x)

    from auth import hash_password
    hash_password = MagicMock(return_value="hashed")

    response = register(user_data, db)
    assert response.username == user_data.username
    assert response.email == user_data.email

@patch("routes.verify_password", return_value=False)
def test_login_invalid_credentials(mock_verify_password):
    db = MagicMock()
    db_user = User(username="testuser", hashed_password="hashed")
    db.query().filter().first.return_value = db_user

    from auth import verify_password
    verify_password = MagicMock(return_value=False)

    with pytest.raises(HTTPException) as exc_info:
        login(UserAuth(username="testuser", password="wrong"), db)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid credentials"


def test_update_profile_success():
    db = MagicMock()
    user = User(username="testuser", first_name="Old", last_name="Name")
    db.query().filter().first.return_value = user

    update_data = UserUpdate(first_name="New", last_name="User")

    updated_user = update_profile(update_data, db, username="testuser")
    assert updated_user.first_name == "New"
    assert updated_user.last_name == "User"

