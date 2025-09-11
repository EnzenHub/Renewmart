from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class NotificationType(str, enum.Enum):
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    APPROVAL_REQUIRED = "approval_required"
    APPROVAL_DECISION = "approval_decision"
    MILESTONE_REACHED = "milestone_reached"
    DEADLINE_REMINDER = "deadline_reminder"
    SLA_BREACH = "sla_breach"
    DOCUMENT_UPLOADED = "document_uploaded"
    STATUS_CHANGE = "status_change"

class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    WEB_PUSH = "web_push"
    IN_APP = "in_app"

class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    message = Column(Text)
    notification_type = Column(Enum(NotificationType))
    channel = Column(Enum(NotificationChannel))
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    
    # Recipient
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", foreign_keys=[user_id], back_populates="received_notifications")
    
    # Related entities
    related_entity_type = Column(String)  # e.g., "task", "proposal", "project"
    related_entity_id = Column(Integer)
    
    # Notification data
    data = Column(JSON)  # Additional data for the notification
    
    # Delivery tracking
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    failed_reason = Column(Text)
    
    # Retry mechanism
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    notification_type = Column(Enum(NotificationType))
    channel = Column(Enum(NotificationChannel))
    
    # Template content
    subject_template = Column(String)  # For email
    message_template = Column(Text)
    
    # Template variables
    variables = Column(JSON)  # List of required variables
    
    # Template configuration
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=1)  # 1 = high, 2 = medium, 3 = low
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
