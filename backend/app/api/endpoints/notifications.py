from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.notification import Notification, NotificationStatus, NotificationType, NotificationChannel
from app.schemas.notification import (
    Notification as NotificationSchema,
    NotificationCreate,
    NotificationUpdate
)
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[NotificationSchema])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[NotificationStatus] = None,
    notification_type: Optional[NotificationType] = None,
    channel: Optional[NotificationChannel] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notifications for the current user"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if status:
        query = query.filter(Notification.status == status)
    if notification_type:
        query = query.filter(Notification.notification_type == notification_type)
    if channel:
        query = query.filter(Notification.channel == channel)
    
    notifications = query.offset(skip).limit(limit).order_by(Notification.created_at.desc()).all()
    return notifications

@router.get("/unread", response_model=List[NotificationSchema])
async def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get unread notifications for the current user"""
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status.in_([NotificationStatus.PENDING, NotificationStatus.SENT, NotificationStatus.DELIVERED])
    ).order_by(Notification.created_at.desc()).all()
    return notifications

@router.get("/{notification_id}", response_model=NotificationSchema)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notification by ID"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/", response_model=NotificationSchema)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new notification"""
    # Only admins and system can create notifications
    if current_user.user_type.value not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create notifications")
    
    notification_data = notification.dict()
    notification_data["created_by"] = current_user.id
    
    db_notification = Notification(**notification_data)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.patch("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.status = NotificationStatus.READ
    notification.read_at = datetime.utcnow()
    
    db.commit()
    db.refresh(notification)
    
    return {"message": "Notification marked as read"}

@router.patch("/{notification_id}/unread")
async def mark_notification_unread(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark notification as unread"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.status = NotificationStatus.DELIVERED
    notification.read_at = None
    
    db.commit()
    db.refresh(notification)
    
    return {"message": "Notification marked as unread"}

@router.patch("/read-all")
async def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read for the current user"""
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status.in_([NotificationStatus.PENDING, NotificationStatus.SENT, NotificationStatus.DELIVERED])
    ).all()
    
    for notification in notifications:
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": f"Marked {len(notifications)} notifications as read"}

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete notification by ID"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted successfully"}

@router.delete("/")
async def delete_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete all notifications for the current user"""
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).all()
    
    for notification in notifications:
        db.delete(notification)
    
    db.commit()
    
    return {"message": f"Deleted {len(notifications)} notifications"}

@router.get("/stats/summary")
async def get_notification_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notification statistics for the current user"""
    total_notifications = db.query(Notification).filter(Notification.user_id == current_user.id).count()
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status.in_([NotificationStatus.PENDING, NotificationStatus.SENT, NotificationStatus.DELIVERED])
    ).count()
    read_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status == NotificationStatus.READ
    ).count()
    
    # Get notifications by type
    type_stats = {}
    for notification_type in NotificationType:
        count = db.query(Notification).filter(
            Notification.user_id == current_user.id,
            Notification.notification_type == notification_type
        ).count()
        type_stats[notification_type.value] = count
    
    return {
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "read_notifications": read_notifications,
        "by_type": type_stats
    }

@router.post("/send/bulk")
async def send_bulk_notifications(
    user_ids: List[int],
    notification_type: NotificationType,
    channel: NotificationChannel,
    title: str,
    message: str,
    data: Optional[dict] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send bulk notifications to multiple users"""
    # Only admins can send bulk notifications
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to send bulk notifications")
    
    notifications = []
    for user_id in user_ids:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            continue
        
        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            user_id=user_id,
            data=data or {},
            created_by=current_user.id
        )
        notifications.append(notification)
    
    db.add_all(notifications)
    db.commit()
    
    return {
        "message": f"Sent {len(notifications)} notifications",
        "sent_count": len(notifications),
        "requested_count": len(user_ids)
    }

@router.post("/send/user/{user_id}")
async def send_notification_to_user(
    user_id: int,
    notification_type: NotificationType,
    channel: NotificationChannel,
    title: str,
    message: str,
    data: Optional[dict] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send notification to a specific user"""
    # Only admins can send notifications
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to send notifications")
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    notification = Notification(
        title=title,
        message=message,
        notification_type=notification_type,
        channel=channel,
        user_id=user_id,
        data=data or {},
        created_by=current_user.id
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return {
        "message": "Notification sent successfully",
        "notification": NotificationSchema.from_orm(notification)
    }
