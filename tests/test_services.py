"""
Service layer tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.services.user_service import UserService
from app.services.opportunity_service import OpportunityService
from app.schemas.user import UserCreate, UserPreferencesCreate
from app.schemas.opportunity import OpportunityCreate
from app.db.models import UserType, OpportunityType

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_services.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_user_service_create_user(db_session):
    """Test user creation in UserService"""
    user_service = UserService(db_session)
    
    user_data = UserCreate(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        user_type=UserType.STUDENT,
        language="en"
    )
    
    user = user_service.create_user(user_data)
    assert user.first_name == "Test"
    assert user.email == "test@example.com"
    assert user.user_type == UserType.STUDENT

def test_user_service_get_user(db_session):
    """Test getting user by ID"""
    user_service = UserService(db_session)
    
    # Create a user first
    user_data = UserCreate(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        user_type=UserType.STUDENT,
        language="en"
    )
    created_user = user_service.create_user(user_data)
    
    # Get the user
    retrieved_user = user_service.get_user(created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.id == created_user.id
    assert retrieved_user.first_name == "Test"

def test_opportunity_service_create_opportunity(db_session):
    """Test opportunity creation in OpportunityService"""
    opportunity_service = OpportunityService(db_session)
    
    opportunity_data = OpportunityCreate(
        title="Test Scholarship",
        description="A test scholarship opportunity",
        opportunity_type=OpportunityType.SCHOLARSHIP,
        organization="Test University",
        language="en",
        tags=["test", "scholarship"],
        requirements=["GPA 3.0+"],
        benefits=["$5000 funding"]
    )
    
    opportunity = opportunity_service.create_opportunity(opportunity_data, creator_id=1)
    assert opportunity.title == "Test Scholarship"
    assert opportunity.opportunity_type == OpportunityType.SCHOLARSHIP
    assert opportunity.created_by == 1

def test_opportunity_service_search(db_session):
    """Test opportunity search"""
    opportunity_service = OpportunityService(db_session)
    
    # Create test opportunities
    opp1_data = OpportunityCreate(
        title="AI Scholarship",
        description="Scholarship for AI research",
        opportunity_type=OpportunityType.SCHOLARSHIP,
        organization="AI University",
        language="en",
        tags=["AI", "research"],
        requirements=[],
        benefits=[]
    )
    
    opp2_data = OpportunityCreate(
        title="Python Course",
        description="Free Python programming course",
        opportunity_type=OpportunityType.LEARNING_RESOURCE,
        organization="Code Academy",
        language="en",
        tags=["Python", "programming"],
        requirements=[],
        benefits=[]
    )
    
    opportunity_service.create_opportunity(opp1_data, creator_id=1)
    opportunity_service.create_opportunity(opp2_data, creator_id=1)
    
    # Search for opportunities
    from app.schemas.opportunity import OpportunitySearch
    search = OpportunitySearch(query="AI")
    results = opportunity_service.search_opportunities(search)
    
    assert len(results) >= 1
    assert any("AI" in opp.title for opp in results)