import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any
from app.config import BOT_TOKEN

def verify_telegram_login(data: Dict[str, Any]) -> bool:
    """
    Verify Telegram login data integrity and authenticity
    
    Args:
        data (Dict[str, Any]): Telegram login data
    
    Returns:
        bool: Whether the login data is valid
    """
    # Extract user data
    user_data = data.get('user', {})
    
    # Check if required fields are present
    required_fields = ['id', 'first_name', 'auth_date', 'hash']
    if not all(field in user_data for field in required_fields):
        return False
    
    # Create data-check-string (sorted alphabetically)
    check_data = {
        k: v for k, v in user_data.items() 
        if k != 'hash' and k != 'photo_url'
    }
    
    # Sort keys alphabetically
    sorted_keys = sorted(check_data.keys())
    
    # Create data-check-string
    data_check_string = '\n'.join([f"{k}={check_data[k]}" for k in sorted_keys])
    
    # Create secret key (SHA256 hash of bot token)
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    
    # Create HMAC signature
    signature = hmac.new(
        secret_key, 
        data_check_string.encode(), 
        hashlib.sha256
    ).hexdigest()
    
    # Check signature
    if signature != user_data['hash']:
        return False
    
    # Check auth date (optional, prevents old login attempts)
    auth_date = int(user_data['auth_date'])
    current_time = int(datetime.utcnow().timestamp())
    
    # Allow login within last 5 minutes
    if current_time - auth_date > 300:
        return False
    
    return True
