from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.user import User
from app.models.project import DevelopmentProject, ProjectStatus, ProjectType
from app.models.land_parcel import Milestone
from app.models.land_parcel import Task, TaskStatus
from app.schemas.project import (
    DevelopmentProject as ProjectSchema, 
    DevelopmentProjectCreate, 
    DevelopmentProjectUpdate
)
from app.schemas.land_parcel import (
    Milestone as MilestoneSchema,
    MilestoneCreate,
    Task as TaskSchema,
    TaskCreate
)
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = None,
    project_type: Optional[ProjectType] = None,
    project_manager_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all development projects with optional filtering"""
    query = db.query(DevelopmentProject)
    
    if status:
        query = query.filter(DevelopmentProject.status == status)
    if project_type:
        query = query.filter(DevelopmentProject.project_type == project_type)
    if project_manager_id:
        query = query.filter(DevelopmentProject.project_manager_id == project_manager_id)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get development project by ID"""
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    return project

@router.post("/", response_model=ProjectSchema)
async def create_project(
    project: DevelopmentProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new development project"""
    # Only project managers and admins can create projects
    if current_user.user_type.value not in ["project_manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create projects")
    
    db_project = DevelopmentProject(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.post("/proposals/{proposal_id}/projects", response_model=ProjectSchema)
async def create_project_from_proposal(
    proposal_id: int,
    project: DevelopmentProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a development project from an approved proposal"""
    # Verify proposal exists and is approved
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    if proposal.status != ProposalStatus.AGREEMENT_SIGNED:
        raise HTTPException(status_code=400, detail="Only proposals with signed agreements can create projects")
    
    # Only project managers and admins can create projects
    if current_user.user_type.value not in ["project_manager", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create projects")
    
    project_data = project.dict()
    project_data["proposal_id"] = proposal_id
    
    db_project = DevelopmentProject(**project_data)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Auto-create initial milestones based on project type
    await create_initial_milestones(db_project.id, db)
    
    return db_project

@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    project_id: int,
    project_update: DevelopmentProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update development project by ID"""
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    
    # Check authorization
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    
    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.patch("/{project_id}/status")
async def update_project_status(
    project_id: int,
    new_status: ProjectStatus,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update project status"""
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    
    # Check authorization
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin", "governance"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this project")
    
    # Validate status transition
    valid_transitions = {
        ProjectStatus.INITIATED: [ProjectStatus.IN_PROGRESS, ProjectStatus.CANCELLED],
        ProjectStatus.IN_PROGRESS: [ProjectStatus.STAGE_GATE, ProjectStatus.CANCELLED],
        ProjectStatus.STAGE_GATE: [ProjectStatus.READY_TO_BUILD, ProjectStatus.IN_PROGRESS, ProjectStatus.CANCELLED],
        ProjectStatus.READY_TO_BUILD: [ProjectStatus.COMPLETED],
        ProjectStatus.CANCELLED: [],
        ProjectStatus.COMPLETED: []
    }
    
    if new_status not in valid_transitions.get(project.status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status transition from {project.status} to {new_status}"
        )
    
    project.status = new_status
    if new_status == ProjectStatus.COMPLETED:
        project.actual_completion_date = datetime.utcnow()
    
    if comments:
        project.description += f"\n\nStatus Update: {comments}"
    
    db.commit()
    db.refresh(project)
    
    return {
        "message": f"Project status updated to {new_status}",
        "project": ProjectSchema.from_orm(project)
    }

@router.get("/{project_id}/milestones", response_model=List[MilestoneSchema])
async def get_project_milestones(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get milestones for a project"""
    milestones = db.query(Milestone).filter(Milestone.project_id == project_id).all()
    return milestones

@router.post("/{project_id}/milestones", response_model=MilestoneSchema)
async def create_project_milestone(
    project_id: int,
    milestone: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a milestone for a project"""
    # Verify project exists
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    
    # Check authorization
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to create milestones for this project")
    
    milestone_data = milestone.dict()
    milestone_data["project_id"] = project_id
    
    db_milestone = Milestone(**milestone_data)
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.post("/{project_id}/milestones/{milestone_id}/submit")
async def submit_milestone(
    project_id: int,
    milestone_id: int,
    submission_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit milestone for approval"""
    milestone = db.query(Milestone).filter(
        Milestone.id == milestone_id,
        Milestone.project_id == project_id
    ).first()
    
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    # Check authorization
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to submit this milestone")
    
    milestone.status = MilestoneStatus.IN_PROGRESS
    if submission_notes:
        milestone.description += f"\n\nSubmission Notes: {submission_notes}"
    
    db.commit()
    db.refresh(milestone)
    
    return {
        "message": "Milestone submitted for approval",
        "milestone": MilestoneSchema.from_orm(milestone)
    }

@router.get("/{project_id}/tasks", response_model=List[TaskSchema])
async def get_project_tasks(
    project_id: int,
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks for a project"""
    query = db.query(Task).filter(Task.project_id == project_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.all()
    return tasks

@router.post("/{project_id}/tasks/assign", response_model=TaskSchema)
async def assign_task_to_project(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign a task to a project"""
    # Verify project exists
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    
    # Check authorization
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to assign tasks to this project")
    
    task_data = task.dict()
    task_data["project_id"] = project_id
    
    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete development project by ID"""
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Development project not found")
    
    # Check authorization
    if (project.project_manager_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")
    
    # Only allow deletion of initiated projects
    if project.status != ProjectStatus.INITIATED:
        raise HTTPException(status_code=400, detail="Only initiated projects can be deleted")
    
    db.delete(project)
    db.commit()
    
    return {"message": "Development project deleted successfully"}

async def create_initial_milestones(project_id: int, db: Session):
    """Create initial milestones for a project based on its type"""
    project = db.query(DevelopmentProject).filter(DevelopmentProject.id == project_id).first()
    if not project:
        return
    
    # Define milestone templates based on project type
    milestone_templates = {
        ProjectType.SOLAR: [
            {"title": "Site Assessment", "description": "Complete site assessment and feasibility study", "order": 1, "estimated_days": 30},
            {"title": "Permit Acquisition", "description": "Obtain all required permits and approvals", "order": 2, "estimated_days": 60},
            {"title": "Design & Engineering", "description": "Complete detailed design and engineering", "order": 3, "estimated_days": 45},
            {"title": "Construction Ready", "description": "Project ready for construction phase", "order": 4, "estimated_days": 30}
        ],
        ProjectType.WIND: [
            {"title": "Wind Resource Assessment", "description": "Complete wind resource assessment", "order": 1, "estimated_days": 45},
            {"title": "Environmental Impact", "description": "Complete environmental impact assessment", "order": 2, "estimated_days": 90},
            {"title": "Permit Acquisition", "description": "Obtain all required permits and approvals", "order": 3, "estimated_days": 120},
            {"title": "Construction Ready", "description": "Project ready for construction phase", "order": 4, "estimated_days": 60}
        ]
    }
    
    templates = milestone_templates.get(project.project_type, milestone_templates[ProjectType.SOLAR])
    
    for template in templates:
        milestone = Milestone(
            title=template["title"],
            description=template["description"],
            order=template["order"],
            project_id=project_id,
            target_date=datetime.utcnow() + timedelta(days=template["estimated_days"]),
            created_by=project.project_manager_id
        )
        db.add(milestone)
    
    db.commit()
