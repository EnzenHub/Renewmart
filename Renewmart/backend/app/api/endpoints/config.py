from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.user import User
from app.models.project import TemplateProject, TemplateMilestone, TemplateTask, ApprovalRule
from app.models.notification import NotificationTemplate
from app.schemas.project import (
    TemplateProject as TemplateProjectSchema,
    TemplateProjectCreate,
    TemplateProjectUpdate,
    TemplateMilestone as TemplateMilestoneSchema,
    TemplateMilestoneCreate,
    TemplateMilestoneUpdate,
    TemplateTask as TemplateTaskSchema,
    TemplateTaskCreate,
    TemplateTaskUpdate,
    ApprovalRule as ApprovalRuleSchema,
    ApprovalRuleCreate,
    ApprovalRuleUpdate
)
from app.schemas.notification import (
    NotificationTemplate as NotificationTemplateSchema,
    NotificationTemplateCreate,
    NotificationTemplateUpdate
)
from app.api.endpoints.auth import get_current_user

router = APIRouter()

# Template Project Management
@router.get("/project-types", response_model=List[TemplateProjectSchema])
async def get_project_types(
    skip: int = 0,
    limit: int = 100,
    project_type: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all project type templates"""
    query = db.query(TemplateProject)
    
    if project_type:
        query = query.filter(TemplateProject.project_type == project_type)
    if region:
        query = query.filter(TemplateProject.region.ilike(f"%{region}%"))
    
    templates = query.offset(skip).limit(limit).all()
    return templates

@router.post("/project-types", response_model=TemplateProjectSchema)
async def create_project_type(
    template: TemplateProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project type template"""
    # Only admins can create project templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create project templates")
    
    template_data = template.dict()
    template_data["created_by"] = current_user.id
    
    db_template = TemplateProject(**template_data)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/project-types/{template_id}", response_model=TemplateProjectSchema)
async def update_project_type(
    template_id: int,
    template_update: TemplateProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update project type template"""
    # Only admins can update project templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update project templates")
    
    template = db.query(TemplateProject).filter(TemplateProject.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Project template not found")
    
    for field, value in template_update.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template

# Template Task Management
@router.get("/templates", response_model=List[TemplateTaskSchema])
async def get_task_templates(
    skip: int = 0,
    limit: int = 100,
    task_type: Optional[str] = None,
    template_project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all task templates"""
    query = db.query(TemplateTask)
    
    if task_type:
        query = query.filter(TemplateTask.task_type == task_type)
    if template_project_id:
        query = query.filter(TemplateTask.template_project_id == template_project_id)
    
    templates = query.offset(skip).limit(limit).all()
    return templates

@router.post("/templates", response_model=TemplateTaskSchema)
async def create_task_template(
    template: TemplateTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task template"""
    # Only admins can create task templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create task templates")
    
    template_data = template.dict()
    template_data["created_by"] = current_user.id
    
    db_template = TemplateTask(**template_data)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/templates/{template_id}", response_model=TemplateTaskSchema)
async def update_task_template(
    template_id: int,
    template_update: TemplateTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task template"""
    # Only admins can update task templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update task templates")
    
    template = db.query(TemplateTask).filter(TemplateTask.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Task template not found")
    
    for field, value in template_update.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template

# Approval Rules Management
@router.get("/approval-rules", response_model=List[ApprovalRuleSchema])
async def get_approval_rules(
    skip: int = 0,
    limit: int = 100,
    project_type: Optional[str] = None,
    region: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all approval rules"""
    query = db.query(ApprovalRule)
    
    if project_type:
        query = query.filter(ApprovalRule.project_type == project_type)
    if region:
        query = query.filter(ApprovalRule.region.ilike(f"%{region}%"))
    if is_active is not None:
        query = query.filter(ApprovalRule.is_active == is_active)
    
    rules = query.offset(skip).limit(limit).all()
    return rules

@router.post("/approval-rules", response_model=ApprovalRuleSchema)
async def create_approval_rule(
    rule: ApprovalRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new approval rule"""
    # Only admins can create approval rules
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create approval rules")
    
    rule_data = rule.dict()
    rule_data["created_by"] = current_user.id
    
    db_rule = ApprovalRule(**rule_data)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.put("/approval-rules/{rule_id}", response_model=ApprovalRuleSchema)
async def update_approval_rule(
    rule_id: int,
    rule_update: ApprovalRuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update approval rule"""
    # Only admins can update approval rules
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update approval rules")
    
    rule = db.query(ApprovalRule).filter(ApprovalRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Approval rule not found")
    
    for field, value in rule_update.dict(exclude_unset=True).items():
        setattr(rule, field, value)
    
    db.commit()
    db.refresh(rule)
    return rule

@router.delete("/approval-rules/{rule_id}")
async def delete_approval_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete approval rule"""
    # Only admins can delete approval rules
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete approval rules")
    
    rule = db.query(ApprovalRule).filter(ApprovalRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Approval rule not found")
    
    db.delete(rule)
    db.commit()
    
    return {"message": "Approval rule deleted successfully"}

# Notification Template Management
@router.get("/notification-templates", response_model=List[NotificationTemplateSchema])
async def get_notification_templates(
    skip: int = 0,
    limit: int = 100,
    notification_type: Optional[str] = None,
    channel: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all notification templates"""
    query = db.query(NotificationTemplate)
    
    if notification_type:
        query = query.filter(NotificationTemplate.notification_type == notification_type)
    if channel:
        query = query.filter(NotificationTemplate.channel == channel)
    if is_active is not None:
        query = query.filter(NotificationTemplate.is_active == is_active)
    
    templates = query.offset(skip).limit(limit).all()
    return templates

@router.post("/notification-templates", response_model=NotificationTemplateSchema)
async def create_notification_template(
    template: NotificationTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new notification template"""
    # Only admins can create notification templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create notification templates")
    
    template_data = template.dict()
    template_data["created_by"] = current_user.id
    
    db_template = NotificationTemplate(**template_data)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.put("/notification-templates/{template_id}", response_model=NotificationTemplateSchema)
async def update_notification_template(
    template_id: int,
    template_update: NotificationTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update notification template"""
    # Only admins can update notification templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update notification templates")
    
    template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Notification template not found")
    
    for field, value in template_update.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template

@router.delete("/notification-templates/{template_id}")
async def delete_notification_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete notification template"""
    # Only admins can delete notification templates
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete notification templates")
    
    template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Notification template not found")
    
    db.delete(template)
    db.commit()
    
    return {"message": "Notification template deleted successfully"}

# System Configuration
@router.get("/system/health")
async def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get system health status"""
    # Only admins can view system health
    if current_user.user_type.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view system health")
    
    # Get basic system statistics
    total_users = db.query(User).count()
    total_projects = db.query(DevelopmentProject).count()
    total_tasks = db.query(Task).count()
    total_approvals = db.query(Approval).count()
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "statistics": {
            "total_users": total_users,
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "total_approvals": total_approvals
        }
    }
