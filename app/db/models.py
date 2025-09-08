"""
Database models for EduOpportunity Bot
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class UserType(str, enum.Enum):
    """User type enumeration"""
    STUDENT = "student"
    SPONSOR = "sponsor"
    MENTOR = "mentor"
    ADMIN = "admin"


class Platform(str, enum.Enum):
    """Platform enumeration"""
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WHATSAPP = "whatsapp"


class OpportunityType(str, enum.Enum):
    """Opportunity type enumeration"""
    SCHOLARSHIP = "scholarship"
    LEARNING_RESOURCE = "learning_resource"
    EVENT = "event"
    MENTORSHIP = "mentorship"
    FUNDING = "funding"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    user_type = Column(Enum(UserType), nullable=False)
    language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    platforms = relationship("UserPlatform", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)
    subscriptions = relationship("Subscription", back_populates="user")


class UserPlatform(Base):
    """User platform accounts (Telegram, Discord, WhatsApp)"""
    __tablename__ = "user_platforms"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(Enum(Platform), nullable=False)
    platform_user_id = Column(String(255), nullable=False)  # Platform-specific user ID
    username = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="platforms")


class UserPreferences(Base):
    """User preferences for opportunity matching"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    interests = Column(JSON, default=list)  # List of interest tags
    education_level = Column(String(50), nullable=True)
    field_of_study = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    budget_range = Column(String(50), nullable=True)
    notification_frequency = Column(String(20), default="daily")  # daily, weekly, monthly
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")


class Opportunity(Base):
    """Opportunity model (scholarships, resources, events)"""
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    opportunity_type = Column(Enum(OpportunityType), nullable=False)
    organization = Column(String(255), nullable=False)
    url = Column(String(500), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    location = Column(String(100), nullable=True)
    language = Column(String(10), default="en")
    tags = Column(JSON, default=list)  # List of tags for categorization
    requirements = Column(JSON, default=list)  # List of requirements
    benefits = Column(JSON, default=list)  # List of benefits
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("User")
    subscriptions = relationship("Subscription", back_populates="opportunity")


class Subscription(Base):
    """User subscriptions to opportunities"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    opportunity = relationship("Opportunity", back_populates="subscriptions")


class Notification(Base):
    """Notification model for tracking sent notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    platform = Column(Enum(Platform), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User")
    opportunity = relationship("Opportunity")


class BotSession(Base):
    """Bot conversation sessions"""
    __tablename__ = "bot_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(Enum(Platform), nullable=False)
    platform_user_id = Column(String(255), nullable=False)
    session_data = Column(JSON, default=dict)  # Store conversation state
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())