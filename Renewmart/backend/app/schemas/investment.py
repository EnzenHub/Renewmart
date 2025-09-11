from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.investment import OpportunityStatus, ProposalStatus

class InvestmentOpportunityBase(BaseModel):
    title: str
    description: str
    target_capacity_mw: float
    target_region: str
    investment_amount: float
    expected_returns: float
    investor_id: int
    advisor_id: int

class InvestmentOpportunityCreate(InvestmentOpportunityBase):
    pass

class InvestmentOpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[OpportunityStatus] = None
    target_capacity_mw: Optional[float] = None
    target_region: Optional[str] = None
    investment_amount: Optional[float] = None
    expected_returns: Optional[float] = None

class InvestmentOpportunity(InvestmentOpportunityBase):
    id: int
    status: OpportunityStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class InvestmentProposalBase(BaseModel):
    title: str
    description: str
    total_capacity_mw: float
    total_investment: float
    expected_completion_date: Optional[datetime] = None
    opportunity_id: int
    advisor_id: int

class InvestmentProposalCreate(InvestmentProposalBase):
    pass

class InvestmentProposalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProposalStatus] = None
    total_capacity_mw: Optional[float] = None
    total_investment: Optional[float] = None
    expected_completion_date: Optional[datetime] = None

class InvestmentProposal(InvestmentProposalBase):
    id: int
    status: ProposalStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProposalParcelBase(BaseModel):
    proposal_id: int
    land_parcel_id: int
    allocated_capacity_mw: float
    allocated_investment: float
    notes: Optional[str] = None

class ProposalParcelCreate(ProposalParcelBase):
    pass

class ProposalParcelUpdate(BaseModel):
    allocated_capacity_mw: Optional[float] = None
    allocated_investment: Optional[float] = None
    notes: Optional[str] = None

class ProposalParcel(ProposalParcelBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
