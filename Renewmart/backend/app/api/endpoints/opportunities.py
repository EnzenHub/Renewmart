from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.investment import InvestmentOpportunity, OpportunityStatus
from app.schemas.investment import InvestmentOpportunity as OpportunitySchema, InvestmentOpportunityCreate, InvestmentOpportunityUpdate
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[OpportunitySchema])
async def get_opportunities(
    skip: int = 0,
    limit: int = 100,
    status: Optional[OpportunityStatus] = None,
    investor_id: Optional[int] = None,
    advisor_id: Optional[int] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all investment opportunities with optional filtering"""
    query = db.query(InvestmentOpportunity)
    
    if status:
        query = query.filter(InvestmentOpportunity.status == status)
    if investor_id:
        query = query.filter(InvestmentOpportunity.investor_id == investor_id)
    if advisor_id:
        query = query.filter(InvestmentOpportunity.advisor_id == advisor_id)
    if region:
        query = query.filter(InvestmentOpportunity.target_region.ilike(f"%{region}%"))
    
    opportunities = query.offset(skip).limit(limit).all()
    return opportunities

@router.get("/{opportunity_id}", response_model=OpportunitySchema)
async def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get investment opportunity by ID"""
    opportunity = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Investment opportunity not found")
    return opportunity

@router.post("/", response_model=OpportunitySchema)
async def create_opportunity(
    opportunity: InvestmentOpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new investment opportunity"""
    # Only advisors and admins can create opportunities
    if current_user.user_type.value not in ["advisor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create opportunities")
    
    db_opportunity = InvestmentOpportunity(**opportunity.dict())
    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)
    return db_opportunity

@router.put("/{opportunity_id}", response_model=OpportunitySchema)
async def update_opportunity(
    opportunity_id: int,
    opportunity_update: InvestmentOpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update investment opportunity by ID"""
    opportunity = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Investment opportunity not found")
    
    # Check authorization
    if (opportunity.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this opportunity")
    
    for field, value in opportunity_update.dict(exclude_unset=True).items():
        setattr(opportunity, field, value)
    
    db.commit()
    db.refresh(opportunity)
    return opportunity

@router.patch("/{opportunity_id}/state")
async def update_opportunity_status(
    opportunity_id: int,
    new_status: OpportunityStatus,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update opportunity status"""
    opportunity = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Investment opportunity not found")
    
    # Check authorization
    if (opportunity.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin", "governance"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this opportunity")
    
    # Validate status transition
    valid_transitions = {
        OpportunityStatus.DRAFT: [OpportunityStatus.SUBMITTED],
        OpportunityStatus.SUBMITTED: [OpportunityStatus.UNDER_REVIEW, OpportunityStatus.DRAFT],
        OpportunityStatus.UNDER_REVIEW: [OpportunityStatus.APPROVED, OpportunityStatus.REJECTED],
        OpportunityStatus.APPROVED: [OpportunityStatus.EXPIRED],
        OpportunityStatus.REJECTED: [OpportunityStatus.DRAFT],
        OpportunityStatus.EXPIRED: []
    }
    
    if new_status not in valid_transitions.get(opportunity.status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status transition from {opportunity.status} to {new_status}"
        )
    
    opportunity.status = new_status
    if comments:
        opportunity.description += f"\n\nStatus Update: {comments}"
    
    db.commit()
    db.refresh(opportunity)
    
    return {
        "message": f"Opportunity status updated to {new_status}",
        "opportunity": OpportunitySchema.from_orm(opportunity)
    }

@router.delete("/{opportunity_id}")
async def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete investment opportunity by ID"""
    opportunity = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Investment opportunity not found")
    
    # Check authorization
    if (opportunity.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this opportunity")
    
    # Only allow deletion of draft opportunities
    if opportunity.status != OpportunityStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Only draft opportunities can be deleted")
    
    db.delete(opportunity)
    db.commit()
    
    return {"message": "Investment opportunity deleted successfully"}

@router.get("/investor/{investor_id}", response_model=List[OpportunitySchema])
async def get_investor_opportunities(
    investor_id: int,
    status: Optional[OpportunityStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get opportunities for a specific investor"""
    query = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.investor_id == investor_id)
    
    if status:
        query = query.filter(InvestmentOpportunity.status == status)
    
    opportunities = query.all()
    return opportunities

@router.get("/advisor/{advisor_id}", response_model=List[OpportunitySchema])
async def get_advisor_opportunities(
    advisor_id: int,
    status: Optional[OpportunityStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get opportunities created by a specific advisor"""
    query = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.advisor_id == advisor_id)
    
    if status:
        query = query.filter(InvestmentOpportunity.status == status)
    
    opportunities = query.all()
    return opportunities

@router.get("/region/{region}", response_model=List[OpportunitySchema])
async def get_opportunities_by_region(
    region: str,
    status: Optional[OpportunityStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get opportunities by region"""
    query = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.target_region.ilike(f"%{region}%"))
    
    if status:
        query = query.filter(InvestmentOpportunity.status == status)
    
    opportunities = query.all()
    return opportunities
