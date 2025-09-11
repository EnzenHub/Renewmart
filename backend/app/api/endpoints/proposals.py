from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.investment import InvestmentProposal, ProposalStatus, ProposalParcel
from app.schemas.investment import (
    InvestmentProposal as ProposalSchema, 
    InvestmentProposalCreate, 
    InvestmentProposalUpdate,
    ProposalParcel as ProposalParcelSchema,
    ProposalParcelCreate
)
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProposalSchema])
async def get_proposals(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProposalStatus] = None,
    opportunity_id: Optional[int] = None,
    advisor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all investment proposals with optional filtering"""
    query = db.query(InvestmentProposal)
    
    if status:
        query = query.filter(InvestmentProposal.status == status)
    if opportunity_id:
        query = query.filter(InvestmentProposal.opportunity_id == opportunity_id)
    if advisor_id:
        query = query.filter(InvestmentProposal.advisor_id == advisor_id)
    
    proposals = query.offset(skip).limit(limit).all()
    return proposals

@router.get("/{proposal_id}", response_model=ProposalSchema)
async def get_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get investment proposal by ID"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    return proposal

@router.post("/", response_model=ProposalSchema)
async def create_proposal(
    proposal: InvestmentProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new investment proposal"""
    # Only advisors and admins can create proposals
    if current_user.user_type.value not in ["advisor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create proposals")
    
    db_proposal = InvestmentProposal(**proposal.dict())
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

@router.post("/opportunities/{opportunity_id}/proposals", response_model=ProposalSchema)
async def create_proposal_for_opportunity(
    opportunity_id: int,
    proposal: InvestmentProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a proposal for a specific opportunity"""
    # Verify opportunity exists
    opportunity = db.query(InvestmentOpportunity).filter(InvestmentOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Investment opportunity not found")
    
    # Only advisors and admins can create proposals
    if current_user.user_type.value not in ["advisor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create proposals")
    
    proposal_data = proposal.dict()
    proposal_data["opportunity_id"] = opportunity_id
    
    db_proposal = InvestmentProposal(**proposal_data)
    db.add(db_proposal)
    db.commit()
    db.refresh(db_proposal)
    return db_proposal

@router.put("/{proposal_id}", response_model=ProposalSchema)
async def update_proposal(
    proposal_id: int,
    proposal_update: InvestmentProposalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update investment proposal by ID"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    # Check authorization
    if (proposal.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this proposal")
    
    for field, value in proposal_update.dict(exclude_unset=True).items():
        setattr(proposal, field, value)
    
    db.commit()
    db.refresh(proposal)
    return proposal

@router.post("/{proposal_id}/approve")
async def approve_proposal(
    proposal_id: int,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve investment proposal"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    # Check authorization (investors and governance can approve)
    if current_user.user_type.value not in ["investor", "governance", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to approve proposals")
    
    if proposal.status != ProposalStatus.UNDER_REVIEW:
        raise HTTPException(status_code=400, detail="Only proposals under review can be approved")
    
    proposal.status = ProposalStatus.APPROVED
    if comments:
        proposal.description += f"\n\nApproval Comments: {comments}"
    
    db.commit()
    db.refresh(proposal)
    
    return {
        "message": "Proposal approved successfully",
        "proposal": ProposalSchema.from_orm(proposal)
    }

@router.post("/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: int,
    rejection_reason: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject investment proposal"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    # Check authorization (investors and governance can reject)
    if current_user.user_type.value not in ["investor", "governance", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to reject proposals")
    
    if proposal.status != ProposalStatus.UNDER_REVIEW:
        raise HTTPException(status_code=400, detail="Only proposals under review can be rejected")
    
    proposal.status = ProposalStatus.REJECTED
    proposal.description += f"\n\nRejection Reason: {rejection_reason}"
    
    db.commit()
    db.refresh(proposal)
    
    return {
        "message": "Proposal rejected",
        "proposal": ProposalSchema.from_orm(proposal)
    }

@router.post("/{proposal_id}/agreements")
async def create_development_service_agreement(
    proposal_id: int,
    agreement_content: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create Development Service Agreement (DSA) for approved proposal"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    if proposal.status != ProposalStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Only approved proposals can have DSAs created")
    
    # Only advisors and admins can create DSAs
    if current_user.user_type.value not in ["advisor", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized to create DSAs")
    
    # Update proposal status to agreement signed
    proposal.status = ProposalStatus.AGREEMENT_SIGNED
    proposal.description += f"\n\nDSA Created: {agreement_content}"
    
    db.commit()
    db.refresh(proposal)
    
    return {
        "message": "Development Service Agreement created successfully",
        "proposal": ProposalSchema.from_orm(proposal)
    }

@router.get("/{proposal_id}/parcels", response_model=List[ProposalParcelSchema])
async def get_proposal_parcels(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get parcels associated with a proposal"""
    parcels = db.query(ProposalParcel).filter(ProposalParcel.proposal_id == proposal_id).all()
    return parcels

@router.post("/{proposal_id}/parcels", response_model=ProposalParcelSchema)
async def add_parcel_to_proposal(
    proposal_id: int,
    parcel: ProposalParcelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a land parcel to a proposal"""
    # Verify proposal exists
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    # Check authorization
    if (proposal.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to modify this proposal")
    
    parcel_data = parcel.dict()
    parcel_data["proposal_id"] = proposal_id
    
    db_parcel = ProposalParcel(**parcel_data)
    db.add(db_parcel)
    db.commit()
    db.refresh(db_parcel)
    return db_parcel

@router.delete("/{proposal_id}")
async def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete investment proposal by ID"""
    proposal = db.query(InvestmentProposal).filter(InvestmentProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Investment proposal not found")
    
    # Check authorization
    if (proposal.advisor_id != current_user.id and 
        current_user.user_type.value not in ["admin"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this proposal")
    
    # Only allow deletion of draft proposals
    if proposal.status != ProposalStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Only draft proposals can be deleted")
    
    db.delete(proposal)
    db.commit()
    
    return {"message": "Investment proposal deleted successfully"}
