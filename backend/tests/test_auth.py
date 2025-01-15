"""
Test auth endpoints.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.utils.access_token import decode_token
from app.web.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "login_data",
    [
        {
            "login_type": "tg_login_widget",
            "credentials": {
                "id": 1359415063,
                "first_name": "StrawBerry🍓",
                "username": "Teri_anric",
                "photo_url": "https://t.me/i/userpic/320/MaU8a600OweaLv9zwY4NIXOp7zbGb_IZCSadIFSzkaY.jpg",
                "auth_date": 1736188397,
                "hash": "a056dc18898ce6501cce0b1e4e7aa7f299a7bfab739631f4a3f8b0f505c61289",
            },
        }
    ],
)
def test_telegram_login_success(db_session: Session, login_data: dict):
    """Test Telegram login endpoint."""
    with patch(
        "app.db.repos.user.UserRepository.create_or_update_user"
    ) as mock_create_or_update_user:
        mock_create_or_update_user.return_value = User(
            id=61289, telegram_id=login_data["credentials"]["id"]
        )
        print(login_data)
        with patch("app.web.api.auth.verify_telegram_login", return_value=True):
            response = client.post("/api/auth/login", json=login_data)

        # Check response status code
        assert (
            response.status_code == 200
        ), f"Login failed with status code {response.status_code}"

        data = response.json()

        # Check access token
        assert "access_token" in data, "Access token is missing in the response"
        decoded_token = decode_token(data["access_token"])
        assert (
            decoded_token["sub"] == login_data["credentials"]["id"]
        ), "User ID mismatch"

        # Check user data
        assert "user" in data, "User data is missing in the response"
        assert (
            data["user"]["telegram_id"] == login_data["credentials"]["id"]
        ), "User ID mismatch"

        mock_create_or_update_user.assert_called_once()


@pytest.mark.parametrize(
    "status_code, login_data",
    [
        (
            400,
            {
                "login_type": "tg_login_widget",
                "credentials": {
                    "id": "123456789",
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "photo_url": "https://example.com/photo.jpg",
                    "auth_date": 1715155200,
                    "hash": "1234567890",
                },  # Not valid telegram login data(hash is not valid)
            },
        ),
    ],
)
def test_telegram_login_failure(
    db_session: Session, status_code: int, login_data: dict
):
    """Test Telegram login endpoint not valid telegram login data."""
    with patch("app.web.api.auth.verify_telegram_login", return_value=False):
        response = client.post("/api/auth/login", json=login_data)
    assert (
        response.status_code == status_code
    ), f"Login failed with status code {response.status_code}"
