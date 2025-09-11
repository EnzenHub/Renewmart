from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class ParcelStatus(str, enum.Enum):
    REGISTERED = "registered"
    FEASIBILITY_ASSIGNED = "feasibility_assigned"
    FEASIBILITY_IN_PROGRESS = "feasibility_in_progress"
    FEASIBILITY_COMPLETED = "feasibility_completed"
    FEASIBILITY_APPROVED = "feasibility_approved"
    FEASIBILITY_REJECTED = "feasibility_rejected"
    READY_FOR_PROPOSAL = "ready_for_proposal"
    IN_PROPOSAL = "in_proposal"
    IN_DEVELOPMENT = "in_development"
    READY_TO_BUILD = "ready_to_build"

class LandParcel(Base):
    __tablename__ = "land_parcels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    size_acres = Column(Float)
    coordinates = Column(JSON)  # Store lat/lng as JSON
    description = Column(Text)
    status = Column(Enum(ParcelStatus), default=ParcelStatus.REGISTERED)
    
    # Ownership
    landowner_id = Column(Integer, ForeignKey("users.id"), index=True)
    landowner = relationship("User", back_populates="land_parcels")
    
    # Feasibility
    feasibility_completed = Column(Boolean, default=False)
    feasibility_score = Column(Float)
    feasibility_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    documents = relationship("Document", back_populates="land_parcel")
    tasks = relationship("Task", back_populates="land_parcel")
    proposal_parcels = relationship("ProposalParcel", back_populates="land_parcel")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    mime_type = Column(String)
    document_type = Column(String)  # e.g., "feasibility_report", "agreement", "permit"
    checksum = Column(String)  # For integrity verification
    
    # Relationships
    land_parcel_id = Column(Integer, ForeignKey("land_parcels.id"), nullable=True)
    land_parcel = relationship("LandParcel", back_populates="documents")
    
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    task = relationship("Task", back_populates="documents")
    
    project_id = Column(Integer, ForeignKey("development_projects.id"), nullable=True)
    project = relationship("DevelopmentProject", back_populates="documents")
    
    proposal_id = Column(Integer, ForeignKey("investment_proposals.id"), nullable=True)
    proposal = relationship("InvestmentProposal", back_populates="documents")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    
    # Assignment
    assigned_to = Column(Integer, ForeignKey("users.id"), index=True)
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    
    # Due dates
    due_date = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    land_parcel_id = Column(Integer, ForeignKey("land_parcels.id"), nullable=True)
    land_parcel = relationship("LandParcel", back_populates="tasks")
    
    project_id = Column(Integer, ForeignKey("development_projects.id"), nullable=True)
    project = relationship("DevelopmentProject", back_populates="tasks")
    
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    milestone = relationship("Milestone", back_populates="tasks")
    
    documents = relationship("Document", back_populates="task")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class Approval(Base):
    __tablename__ = "approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    approval_type = Column(String)  # e.g., "feasibility", "proposal", "milestone"
    status = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    comments = Column(Text)
    
    # Approver
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime)
    
    # Relationships
    land_parcel_id = Column(Integer, ForeignKey("land_parcels.id"), nullable=True)
    proposal_id = Column(Integer, ForeignKey("investment_proposals.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("development_projects.id"), nullable=True)
    milestone_id = Column(Integer, ForeignKey("milestones.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class MilestoneStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    APPROVED = "approved"
    REJECTED = "rejected"

class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    status = Column(Enum(MilestoneStatus), default=MilestoneStatus.PENDING)
    
    # Dates
    target_date = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    project_id = Column(Integer, ForeignKey("development_projects.id"), index=True)
    project = relationship("DevelopmentProject", back_populates="milestones")
    
    tasks = relationship("Task", back_populates="milestone")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
