"""
Telegram login verification.
"""

import hashlib
import hmac
from typing import Any, Dict

from app.config import settings


def verify_telegram_login(data: Dict[str, Any]) -> bool:
    """
    Verify Telegram login data integrity and authenticity

    Args:
        data (Dict[str, Any]): Telegram login data

    Returns:
        bool: Whether the login data is valid
    """
    if not data.get("hash"):
        return False

    # Create data-check-string (sorted alphabetically)
    check_data = {k: v for k, v in data.items() if k != "hash" and k != "photo_url"}

    # Sort keys alphabetically
    sorted_keys = sorted(check_data.keys())

    # Create data-check-string
    data_check_string = "\n".join([f"{k}={check_data[k]}" for k in sorted_keys])

    # Create secret key (SHA256 hash of bot token)
    secret_key = hashlib.sha256(settings.bot_token.encode()).digest()

    # Create HMAC signature
    signature = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    # Check signature
    if signature != data["hash"]:
        return False

    # # Check auth date (optional, prevents old login attempts)
    # auth_date = int(data['auth_date'])
    # current_time = int(datetime.utcnow().timestamp())

    # # Allow login within last 5 minutes
    # if current_time - auth_date > 300:
    #     return False

    return True
