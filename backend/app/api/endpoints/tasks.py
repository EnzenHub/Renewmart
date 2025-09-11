from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.land_parcel import Task, TaskStatus
from app.schemas.land_parcel import Task as TaskSchema, TaskCreate, TaskUpdate
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TaskSchema])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    assignee_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks with optional filtering"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if assignee_id:
        query = query.filter(Task.assigned_to == assignee_id)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/assign")
async def assign_task(
    task_id: int,
    assignee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign task to a user"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify assignee exists
    assignee = db.query(User).filter(User.id == assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    task.assigned_to = assignee_id
    task.status = TaskStatus.ASSIGNED
    db.commit()
    
    return {"message": f"Task assigned to {assignee.name}"}

@router.patch("/{task_id}/accept")
async def accept_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept task assignment"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to accept this task")
    
    task.status = TaskStatus.IN_PROGRESS
    db.commit()
    
    return {"message": "Task accepted and started"}

@router.patch("/{task_id}/complete")
async def complete_task(
    task_id: int,
    completion_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark task as completed"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to complete this task")
    
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.utcnow()
    if completion_notes:
        task.description += f"\n\nCompletion Notes: {completion_notes}"
    
    db.commit()
    
    return {"message": "Task completed successfully"}

@router.patch("/{task_id}/reject")
async def reject_task(
    task_id: int,
    rejection_reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject task assignment"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to reject this task")
    
    task.status = TaskStatus.REJECTED
    task.description += f"\n\nRejection Reason: {rejection_reason}"
    db.commit()
    
    return {"message": "Task rejected"}

@router.get("/assignee/{user_id}", response_model=List[TaskSchema])
async def get_user_tasks(
    user_id: int,
    status: Optional[TaskStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks assigned to a specific user"""
    query = db.query(Task).filter(Task.assigned_to == user_id)
    
    if status:
        query = query.filter(Task.status == status)
    
    tasks = query.all()
    return tasks

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}
