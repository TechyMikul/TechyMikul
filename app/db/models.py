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


# -----------------------------
# Extensions for advanced features
# -----------------------------


class InteractionType(str, enum.Enum):
    """User interactions with opportunities for personalization"""
    CLICK = "click"
    IGNORE = "ignore"
    SHARE = "share"
    SUBSCRIBE = "subscribe"
    APPLY = "apply"


class UserInteraction(Base):
    """Log of user interactions to learn preferences over time"""
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    action = Column(Enum(InteractionType), nullable=False)
    context = Column(JSON, default=dict)  # e.g., platform, message_id
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApplicationStatus(str, enum.Enum):
    """Status of an application to an opportunity"""
    DRAFT = "draft"
    APPLIED = "applied"
    IN_PROGRESS = "in_progress"
    INTERVIEW = "interview"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class OpportunityApplication(Base):
    """Track a user's application to an opportunity"""
    __tablename__ = "opportunity_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, nullable=False)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=True)
    last_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    notes = Column(Text, nullable=True)
    metadata = Column(JSON, default=dict)  # links, submission ids

    # Relationships
    user = relationship("User")
    opportunity = relationship("Opportunity")


class ReminderType(str, enum.Enum):
    DEADLINE = "deadline"
    FOLLOW_UP = "follow_up"
    STATUS_UPDATE = "status_update"


class Reminder(Base):
    """Scheduled reminders (e.g., deadlines)"""
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    reminder_type = Column(Enum(ReminderType), nullable=False)
    remind_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, default=dict)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GroupRole(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"


class CollaborationGroup(Base):
    """Groups for sharing opportunities (scholarships, events, competitions)"""
    __tablename__ = "collab_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")


class GroupMember(Base):
    """Membership of users in collaboration groups"""
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("collab_groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(GroupRole), default=GroupRole.MEMBER, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    group = relationship("CollaborationGroup", back_populates="members")
    user = relationship("User")


class GroupSharedOpportunity(Base):
    """Opportunities shared within a group"""
    __tablename__ = "group_shared_opportunities"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("collab_groups.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=False)
    shared_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Badge(Base):
    """Skill badge definition (verifiable credential-like)"""
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    criteria = Column(Text, nullable=True)
    issuer = Column(String(255), nullable=True)  # org or verifier
    metadata = Column(JSON, default=dict)  # optional blockchain/VC pointers
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserBadge(Base):
    """Badges earned by a user (Skill Passport)"""
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    proof_url = Column(String(500), nullable=True)
    verifier = Column(String(255), nullable=True)
    metadata = Column(JSON, default=dict)

    # Relationships
    user = relationship("User")
    badge = relationship("Badge")


class ChallengeDifficulty(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SkillChallenge(Base):
    """Micro-courses, projects, or challenges for earning badges"""
    __tablename__ = "skill_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(JSON, default=list)
    difficulty = Column(Enum(ChallengeDifficulty), default=ChallengeDifficulty.BEGINNER)
    estimated_hours = Column(Integer, nullable=True)
    reward_badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    reward_badge = relationship("Badge")


class ChallengeStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    VERIFIED = "verified"
    FAILED_VERIFICATION = "failed_verification"


class UserChallengeProgress(Base):
    """User progress on challenges"""
    __tablename__ = "user_challenge_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("skill_challenges.id"), nullable=False)
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.NOT_STARTED)
    started_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    evidence_urls = Column(JSON, default=list)
    reviewer_notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User")
    challenge = relationship("SkillChallenge")