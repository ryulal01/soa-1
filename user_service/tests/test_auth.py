import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.parametrize(
    "username, email, password, status_code",
    [
        ("validUser", "test@example.com", "StrongPass1!", 201),
        ("us", "test@example.com", "StrongPass1!", 422),
        ("invalid user", "test@example.com", "StrongPass1!", 422),
        ("validUser", "invalid-email", "StrongPass1!", 422),
        ("validUser", "test@example.com", "weak", 422),
    ]
)
def test_register_user(username, email, password, status_code):
    response = client.post(
        "/register",
        json={"username": username, "email": email, "password": password}
    )
    assert response.status_code == status_code


def test_login_success():
    client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test123!"
    })
    
    response = client.post("/login", json={
        "username": "testuser",
        "password": "Test123!"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials():
    response = client.post("/login", json={
        "username": "wronguser",
        "password": "WrongPass1!"
    })
    
    assert response.status_code == 400

