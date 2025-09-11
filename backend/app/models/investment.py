from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class OpportunityStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class InvestmentOpportunity(Base):
    __tablename__ = "investment_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(OpportunityStatus), default=OpportunityStatus.DRAFT)
    
    # Investment details
    target_capacity_mw = Column(Float)
    target_region = Column(String)
    investment_amount = Column(Float)
    expected_returns = Column(Float)
    
    # Relationships
    investor_id = Column(Integer, ForeignKey("users.id"), index=True)
    investor = relationship("User", foreign_keys=[investor_id])
    
    advisor_id = Column(Integer, ForeignKey("users.id"), index=True)
    advisor = relationship("User", foreign_keys=[advisor_id], back_populates="created_opportunities")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    proposals = relationship("InvestmentProposal", back_populates="opportunity")

class ProposalStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    AGREEMENT_SIGNED = "agreement_signed"

class InvestmentProposal(Base):
    __tablename__ = "investment_proposals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(ProposalStatus), default=ProposalStatus.DRAFT)
    
    # Proposal details
    total_capacity_mw = Column(Float)
    total_investment = Column(Float)
    expected_completion_date = Column(DateTime)
    
    # Relationships
    opportunity_id = Column(Integer, ForeignKey("investment_opportunities.id"), index=True)
    opportunity = relationship("InvestmentOpportunity", back_populates="proposals")
    
    advisor_id = Column(Integer, ForeignKey("users.id"), index=True)
    advisor = relationship("User", foreign_keys=[advisor_id], back_populates="created_proposals")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    proposal_parcels = relationship("ProposalParcel", back_populates="proposal")
    documents = relationship("Document", back_populates="proposal")
    projects = relationship("DevelopmentProject", back_populates="proposal")

class ProposalParcel(Base):
    __tablename__ = "proposal_parcels"
    
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(Integer, ForeignKey("investment_proposals.id"), index=True)
    land_parcel_id = Column(Integer, ForeignKey("land_parcels.id"), index=True)
    
    # Parcel-specific details in proposal
    allocated_capacity_mw = Column(Float)
    allocated_investment = Column(Float)
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    proposal = relationship("InvestmentProposal", back_populates="proposal_parcels")
    land_parcel = relationship("LandParcel", back_populates="proposal_parcels")
