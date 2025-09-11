from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.user import User
from app.models.land_parcel import LandParcel, ParcelStatus
from app.schemas.land_parcel import LandParcel as LandParcelSchema, LandParcelCreate, LandParcelUpdate
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[LandParcelSchema])
async def get_land_parcels(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ParcelStatus] = None,
    landowner_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all land parcels"""
    query = db.query(LandParcel)
    
    if status:
        query = query.filter(LandParcel.status == status)
    if landowner_id:
        query = query.filter(LandParcel.landowner_id == landowner_id)
    
    parcels = query.offset(skip).limit(limit).all()
    return parcels

@router.get("/{parcel_id}", response_model=LandParcelSchema)
async def get_land_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get land parcel by ID"""
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Land parcel not found")
    return parcel

@router.post("/", response_model=LandParcelSchema)
async def create_land_parcel(
    parcel: LandParcelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new land parcel"""
    # Only landowners and admins can create parcels
    if current_user.user_type.value not in ["landowner", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create land parcels")
    
    # Ensure landowner_id is provided and valid
    if not parcel.landowner_id:
        raise HTTPException(status_code=400, detail="landowner_id is required")
    
    # Verify the landowner exists
    landowner = db.query(User).filter(User.id == parcel.landowner_id).first()
    if not landowner:
        raise HTTPException(status_code=400, detail="Invalid landowner_id: user not found")
    
    # If current user is a landowner, they can only create parcels for themselves
    if current_user.user_type.value == "landowner" and parcel.landowner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Landowners can only create parcels for themselves")
    
    db_parcel = LandParcel(**parcel.dict())
    db.add(db_parcel)
    db.commit()
    db.refresh(db_parcel)
    return db_parcel

@router.put("/{parcel_id}", response_model=LandParcelSchema)
async def update_land_parcel(
    parcel_id: int,
    parcel_update: LandParcelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update land parcel by ID"""
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Land parcel not found")
    
    # Check authorization
    if (parcel.landowner_id != current_user.id and 
        current_user.user_type.value not in ["admin", "advisor"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this parcel")
    
    for field, value in parcel_update.dict(exclude_unset=True).items():
        setattr(parcel, field, value)
    
    db.commit()
    db.refresh(parcel)
    return parcel

@router.delete("/{parcel_id}")
async def delete_land_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete land parcel by ID"""
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Land parcel not found")
    
    # Check authorization
    if (parcel.landowner_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this parcel")
    
    db.delete(parcel)
    db.commit()
    
    return {"message": "Land parcel deleted successfully"}

@router.post("/{parcel_id}/feasibility")
async def assign_feasibility_study(
    parcel_id: int,
    analyst_id: int,
    due_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assign feasibility study to a parcel"""
    # Only advisors and admins can assign feasibility studies
    if current_user.user_type.value not in ["advisor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to assign feasibility studies")
    
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Land parcel not found")
    
    # Update parcel status
    parcel.status = ParcelStatus.FEASIBILITY_ASSIGNED
    
    # Create feasibility task
    from app.models.land_parcel import Task, TaskStatus
    from datetime import datetime, timedelta
    
    task = Task(
        title="Feasibility Study",
        description=f"Conduct feasibility study for {parcel.name}",
        status=TaskStatus.ASSIGNED,
        priority="high",
        assigned_to=analyst_id,
        due_date=datetime.utcnow() + timedelta(days=30) if not due_date else datetime.fromisoformat(due_date),
        land_parcel_id=parcel_id,
        created_by=current_user.id
    )
    
    db.add(task)
    db.commit()
    
    return {"message": "Feasibility study assigned successfully"}

@router.post("/{parcel_id}/state/transitions")
async def update_parcel_status(
    parcel_id: int,
    new_status: ParcelStatus,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update parcel status with state transition validation"""
    parcel = db.query(LandParcel).filter(LandParcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Land parcel not found")
    
    # Check authorization
    if (parcel.landowner_id != current_user.id and 
        current_user.user_type.value not in ["admin", "advisor", "governance"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this parcel")
    
    # Validate status transition
    valid_transitions = {
        ParcelStatus.REGISTERED: [ParcelStatus.FEASIBILITY_ASSIGNED],
        ParcelStatus.FEASIBILITY_ASSIGNED: [ParcelStatus.FEASIBILITY_IN_PROGRESS],
        ParcelStatus.FEASIBILITY_IN_PROGRESS: [ParcelStatus.FEASIBILITY_COMPLETED],
        ParcelStatus.FEASIBILITY_COMPLETED: [ParcelStatus.FEASIBILITY_APPROVED, ParcelStatus.FEASIBILITY_REJECTED],
        ParcelStatus.FEASIBILITY_APPROVED: [ParcelStatus.READY_FOR_PROPOSAL],
        ParcelStatus.READY_FOR_PROPOSAL: [ParcelStatus.IN_PROPOSAL],
        ParcelStatus.IN_PROPOSAL: [ParcelStatus.IN_DEVELOPMENT],
        ParcelStatus.IN_DEVELOPMENT: [ParcelStatus.READY_TO_BUILD]
    }
    
    if new_status not in valid_transitions.get(parcel.status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status transition from {parcel.status} to {new_status}"
        )
    
    parcel.status = new_status
    if comments:
        parcel.description += f"\n\nStatus Update: {comments}"
    
    db.commit()
    db.refresh(parcel)
    
    return {
        "message": f"Parcel status updated to {new_status}",
        "parcel": LandParcelSchema.from_orm(parcel)
    }
