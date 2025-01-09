from fastapi.testclient import TestClient
from app.web.main import app
from app.utils.access_token import decode_token
from app.db.models.user import User
from sqlalchemy.orm import Session

import pytest

client = TestClient(app)


@pytest.mark.parametrize("result_code, login_data", [
    (200, {
        "login_type": "tg_login_widget",
        "credentials": {
            "id": 1359415063,
            "first_name": "StrawBerry🍓",
            "username": "Teri_anric",
            "photo_url": "https://t.me/i/userpic/320/MaU8a600OweaLv9zwY4NIXOp7zbGb_IZCSadIFSzkaY.jpg",
            "auth_date": 1736188397,
            "hash": "a056dc18898ce6501cce0b1e4e7aa7f299a7bfab739631f4a3f8b0f505c61289"
        }
    }),
    (400, {
        "login_type": "tg_login_widget",
        "credentials": {
            "id": "123456789",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "photo_url": "https://example.com/photo.jpg",
            "auth_date": 1715155200,
            "hash": "1234567890"
        }, # Not valid telegram login data(hash is not valid)
    }),
])
def test_telegram_login(db_session: Session, result_code: int, login_data: dict):
    """Test Telegram login endpoint."""
    response = client.post(
        "/auth/login",
        json=login_data
    )
    # Check response status code
    assert response.status_code == result_code, "Login failed"

    if result_code != 200:
        return

    data = response.json()

    # Check access token
    assert "access_token" in data, "Access token is missing in the response"
    decoded_token = decode_token(data["access_token"])
    assert decoded_token["sub"] == login_data["credentials"]["id"], "User ID mismatch"

    # Check user data
    assert "user" in data, "User data is missing in the response"
    assert data["user"]["telegram_id"] == login_data["credentials"]["id"], "User ID mismatch"
    
    # Check user in database
    assert (
        db_session.query(User)
        .filter(User.telegram_id == login_data["credentials"]["id"])
        .first()
        is not None
    ), "User not found in the database"
