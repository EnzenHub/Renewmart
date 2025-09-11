from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.project import ProjectStatus, ProjectType

class DevelopmentProjectBase(BaseModel):
    name: str
    description: str
    project_type: ProjectType
    total_capacity_mw: float
    total_investment: float
    target_completion_date: Optional[datetime] = None
    proposal_id: int
    project_manager_id: int

class DevelopmentProjectCreate(DevelopmentProjectBase):
    pass

class DevelopmentProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    project_type: Optional[ProjectType] = None
    total_capacity_mw: Optional[float] = None
    total_investment: Optional[float] = None
    target_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None

class DevelopmentProject(DevelopmentProjectBase):
    id: int
    status: ProjectStatus
    actual_completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TemplateProjectBase(BaseModel):
    name: str
    description: str
    project_type: ProjectType
    region: str
    size_band_min: float
    size_band_max: float
    config: Dict[str, Any]

class TemplateProjectCreate(TemplateProjectBase):
    created_by: int

class TemplateProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    region: Optional[str] = None
    size_band_min: Optional[float] = None
    size_band_max: Optional[float] = None
    config: Optional[Dict[str, Any]] = None

class TemplateProject(TemplateProjectBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class TemplateMilestoneBase(BaseModel):
    title: str
    description: str
    order: int
    estimated_days: int
    template_project_id: int

class TemplateMilestoneCreate(TemplateMilestoneBase):
    created_by: int

class TemplateMilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    estimated_days: Optional[int] = None

class TemplateMilestone(TemplateMilestoneBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class TemplateTaskBase(BaseModel):
    title: str
    description: str
    task_type: str
    priority: str = "medium"
    estimated_hours: float
    template_project_id: int
    template_milestone_id: Optional[int] = None

class TemplateTaskCreate(TemplateTaskBase):
    created_by: int

class TemplateTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[str] = None
    priority: Optional[str] = None
    estimated_hours: Optional[float] = None
    template_milestone_id: Optional[int] = None

class TemplateTask(TemplateTaskBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class ApprovalRuleBase(BaseModel):
    name: str
    description: str
    project_type: Optional[ProjectType] = None
    region: Optional[str] = None
    size_band_min: Optional[float] = None
    size_band_max: Optional[float] = None
    required_approvers: List[str]
    approval_type: str
    is_active: bool = True
    config: Dict[str, Any]

class ApprovalRuleCreate(ApprovalRuleBase):
    created_by: int

class ApprovalRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    region: Optional[str] = None
    size_band_min: Optional[float] = None
    size_band_max: Optional[float] = None
    required_approvers: Optional[List[str]] = None
    approval_type: Optional[str] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None

class ApprovalRule(ApprovalRuleBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True
