from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.models.land_parcel import ParcelStatus, TaskStatus, ApprovalStatus, MilestoneStatus

class Coordinates(BaseModel):
    lat: float
    lng: float

class LandParcelBase(BaseModel):
    name: str
    address: str
    size_acres: float
    coordinates: Coordinates
    description: Optional[str] = None
    landowner_id: int

class LandParcelCreate(LandParcelBase):
    pass

class LandParcelUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    size_acres: Optional[float] = None
    coordinates: Optional[Coordinates] = None
    description: Optional[str] = None
    status: Optional[ParcelStatus] = None
    feasibility_completed: Optional[bool] = None
    feasibility_score: Optional[float] = None
    feasibility_notes: Optional[str] = None

class LandParcel(LandParcelBase):
    id: int
    status: ParcelStatus
    feasibility_completed: bool
    feasibility_score: Optional[float] = None
    feasibility_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    name: str
    file_path: str
    file_size: int
    mime_type: str
    document_type: str
    checksum: str

class DocumentCreate(DocumentBase):
    land_parcel_id: Optional[int] = None
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    proposal_id: Optional[int] = None
    created_by: int

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    document_type: Optional[str] = None

class Document(DocumentBase):
    id: int
    land_parcel_id: Optional[int] = None
    task_id: Optional[int] = None
    project_id: Optional[int] = None
    proposal_id: Optional[int] = None
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    assigned_to: int
    due_date: Optional[datetime] = None
    land_parcel_id: Optional[int] = None
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None

class TaskCreate(TaskBase):
    created_by: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class Task(TaskBase):
    id: int
    status: TaskStatus
    completed_at: Optional[datetime] = None
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class ApprovalBase(BaseModel):
    approval_type: str
    comments: Optional[str] = None
    land_parcel_id: Optional[int] = None
    proposal_id: Optional[int] = None
    project_id: Optional[int] = None
    milestone_id: Optional[int] = None

class ApprovalCreate(ApprovalBase):
    created_by: int

class ApprovalUpdate(BaseModel):
    status: Optional[ApprovalStatus] = None
    comments: Optional[str] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None

class Approval(ApprovalBase):
    id: int
    status: ApprovalStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class MilestoneBase(BaseModel):
    title: str
    description: str
    target_date: Optional[datetime] = None
    project_id: int

class MilestoneCreate(MilestoneBase):
    created_by: int

class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[MilestoneStatus] = None
    target_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class Milestone(MilestoneBase):
    id: int
    status: MilestoneStatus
    completed_at: Optional[datetime] = None
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True
