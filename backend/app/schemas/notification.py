from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.notification import NotificationType, NotificationChannel, NotificationStatus

class NotificationBase(BaseModel):
    title: str
    message: str
    notification_type: NotificationType
    channel: NotificationChannel
    user_id: int
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[int] = None
    data: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    created_by: int

class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    failed_reason: Optional[str] = None
    retry_count: Optional[int] = None

class Notification(NotificationBase):
    id: int
    status: NotificationStatus
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    failed_reason: Optional[str] = None
    retry_count: int
    max_retries: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class NotificationTemplateBase(BaseModel):
    name: str
    notification_type: NotificationType
    channel: NotificationChannel
    subject_template: str
    message_template: str
    variables: List[str]
    is_active: bool = True
    priority: int = 1

class NotificationTemplateCreate(NotificationTemplateBase):
    created_by: int

class NotificationTemplateUpdate(BaseModel):
    name: Optional[str] = None
    notification_type: Optional[NotificationType] = None
    channel: Optional[NotificationChannel] = None
    subject_template: Optional[str] = None
    message_template: Optional[str] = None
    variables: Optional[List[str]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None

class NotificationTemplate(NotificationTemplateBase):
    id: int
    created_at: datetime
    created_by: int
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
