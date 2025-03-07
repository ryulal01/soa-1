import pytest
from pydantic import ValidationError
from app.schemas import UserCreate

def test_valid_user_create():
    user = UserCreate(username="validUser", email="test@example.com", password="StrongPass1!")
    assert user.username == "validUser"
    assert user.email == "test@example.com"


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("u", "test@example.com", "StrongPass1!"),  # Слишком короткий username
        ("invalid user", "test@example.com", "StrongPass1!"),  # Недопустимые символы в username
        ("validUser", "invalid-email", "StrongPass1!"),  # Некорректный email
        ("validUser", "test@example.com", "weak"),  # Слабый пароль
    ]
)
def test_invalid_user_create(username, email, password):
    with pytest.raises(ValidationError):
        UserCreate(username=username, email=email, password=password)

