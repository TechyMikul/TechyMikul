"""
API tests for EduOpportunity Bot
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.db.models import User, UserType

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Set up test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    """Create a test user"""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "user_type": "student",
        "language": "en"
    }
    response = client.post("/api/v1/users/", json=user_data)
    return response.json()

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "EduOpportunity Bot API" in response.json()["message"]

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_user(setup_database):
    """Test user creation"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "user_type": "student",
        "language": "en"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["email"] == "john@example.com"

def test_get_user(setup_database, test_user):
    """Test getting user by ID"""
    user_id = test_user["id"]
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_create_opportunity(setup_database, test_user):
    """Test opportunity creation"""
    opportunity_data = {
        "title": "Test Scholarship",
        "description": "A test scholarship opportunity",
        "opportunity_type": "scholarship",
        "organization": "Test University",
        "language": "en",
        "tags": ["test", "scholarship"],
        "requirements": ["GPA 3.0+"],
        "benefits": ["$5000 funding"]
    }
    response = client.post("/api/v1/opportunities/", json=opportunity_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Scholarship"

def test_search_opportunities(setup_database):
    """Test opportunity search"""
    response = client.get("/api/v1/opportunities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_webhook_endpoints():
    """Test webhook endpoints"""
    # Test Telegram webhook
    response = client.post("/api/v1/webhooks/telegram", json={"test": "data"})
    assert response.status_code == 200
    
    # Test Discord webhook
    response = client.post("/api/v1/webhooks/discord", json={"test": "data"})
    assert response.status_code == 200
    
    # Test WhatsApp webhook
    response = client.post("/api/v1/webhooks/whatsapp", data={"test": "data"})
    assert response.status_code == 200