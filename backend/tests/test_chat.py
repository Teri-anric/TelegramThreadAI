from fastapi.testclient import TestClient
import pytest
from app.web.main import app
from app.utils.access_token import create_access_token

client = TestClient(app)

@pytest.mark.skip(reason="This test is not implemented yet")
@pytest.mark.parametrize("chat_data", [
    {"title": "Test Chat", "description": "A chat for testing purposes"},
    {"title": "Test Chat 2", "description": "A chat for testing purposes 2"},
])
def test_create_chat(db_session, test_user_data, chat_data):
    """Test creating a new chat."""
    # First, generate an access token
    token = create_access_token(data={"sub": test_user_data["telegram_id"]})
    
    # Send request with authorization
    response = client.post(
        "/chats/", 
        json=chat_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == chat_data["title"]
    assert data["description"] == chat_data["description"]



@pytest.mark.skip(reason="This test is not implemented yet")
def test_get_user_chats(db_session, test_user_data):
    """Test retrieving user's chats."""
    # Generate access token
    token = create_access_token(data={"sub": test_user_data["telegram_id"]})
    
    # Send request to get user chats
    response = client.get(
        "/chats/", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 