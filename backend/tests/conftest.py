"""
Conftest file for backend tests.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create a test database engine
test_engine = create_engine(settings.database.url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test function."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def test_user_data():
    """Test user data."""
    return {"telegram_id": "1234567890", "username": "test_user"}
