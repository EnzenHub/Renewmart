from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.land_parcel import Approval, ApprovalStatus
from app.schemas.land_parcel import Approval as ApprovalSchema, ApprovalCreate, ApprovalUpdate
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ApprovalSchema])
async def get_approvals(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ApprovalStatus] = None,
    approval_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all approvals with optional filtering"""
    query = db.query(Approval)
    
    if status:
        query = query.filter(Approval.status == status)
    if approval_type:
        query = query.filter(Approval.approval_type == approval_type)
    
    approvals = query.offset(skip).limit(limit).all()
    return approvals

@router.get("/pending", response_model=List[ApprovalSchema])
async def get_pending_approvals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all pending approvals"""
    approvals = db.query(Approval).filter(Approval.status == ApprovalStatus.PENDING).all()
    return approvals

@router.get("/{approval_id}", response_model=ApprovalSchema)
async def get_approval(
    approval_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get approval by ID"""
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval

@router.post("/", response_model=ApprovalSchema)
async def create_approval(
    approval: ApprovalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new approval request"""
    db_approval = Approval(**approval.dict())
    db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    return db_approval

@router.post("/{approval_id}/decision")
async def make_approval_decision(
    approval_id: int,
    decision: str,  # "approve" or "reject"
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Make approval decision (approve/reject)"""
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    if approval.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail="Approval is not pending")
    
    # Check if user has permission to approve (governance role)
    if current_user.user_type.value not in ["governance", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to make approval decisions")
    
    if decision.lower() == "approve":
        approval.status = ApprovalStatus.APPROVED
        approval.approved_by = current_user.id
        approval.approved_at = datetime.utcnow()
    elif decision.lower() == "reject":
        approval.status = ApprovalStatus.REJECTED
        approval.approved_by = current_user.id
        approval.approved_at = datetime.utcnow()
    else:
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'reject'")
    
    if comments:
        approval.comments = comments
    
    db.commit()
    db.refresh(approval)
    
    return {
        "message": f"Approval {decision}d successfully",
        "approval": ApprovalSchema.from_orm(approval)
    }

@router.put("/{approval_id}", response_model=ApprovalSchema)
async def update_approval(
    approval_id: int,
    approval_update: ApprovalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update approval by ID"""
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    for field, value in approval_update.dict(exclude_unset=True).items():
        setattr(approval, field, value)
    
    db.commit()
    db.refresh(approval)
    return approval

@router.delete("/{approval_id}")
async def delete_approval(
    approval_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete approval by ID"""
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    db.delete(approval)
    db.commit()
    
    return {"message": "Approval deleted successfully"}

@router.get("/user/{user_id}", response_model=List[ApprovalSchema])
async def get_user_approvals(
    user_id: int,
    status: Optional[ApprovalStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get approvals created by a specific user"""
    query = db.query(Approval).filter(Approval.created_by == user_id)
    
    if status:
        query = query.filter(Approval.status == status)
    
    approvals = query.all()
    return approvals

@router.get("/approver/{user_id}", response_model=List[ApprovalSchema])
async def get_approver_approvals(
    user_id: int,
    status: Optional[ApprovalStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get approvals approved by a specific user"""
    query = db.query(Approval).filter(Approval.approved_by == user_id)
    
    if status:
        query = query.filter(Approval.status == status)
    
    approvals = query.all()
    return approvals

@router.patch("/{approval_id}/cancel")
async def cancel_approval(
    approval_id: int,
    reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a pending approval"""
    approval = db.query(Approval).filter(Approval.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
    
    if approval.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=400, detail="Only pending approvals can be cancelled")
    
    if approval.created_by != current_user.id and current_user.user_type.value not in ["admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this approval")
    
    approval.status = ApprovalStatus.CANCELLED
    approval.comments = f"Cancelled: {reason}"
    db.commit()
    
    return {"message": "Approval cancelled successfully"}
