from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class ProjectStatus(str, enum.Enum):
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    STAGE_GATE = "stage_gate"
    READY_TO_BUILD = "ready_to_build"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ProjectType(str, enum.Enum):
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    STORAGE = "storage"
    HYBRID = "hybrid"

class DevelopmentProject(Base):
    __tablename__ = "development_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.INITIATED)
    project_type = Column(Enum(ProjectType))
    
    # Project details
    total_capacity_mw = Column(Float)
    total_investment = Column(Float)
    target_completion_date = Column(DateTime)
    actual_completion_date = Column(DateTime)
    
    # Relationships
    proposal_id = Column(Integer, ForeignKey("investment_proposals.id"), index=True)
    proposal = relationship("InvestmentProposal", back_populates="projects")
    
    project_manager_id = Column(Integer, ForeignKey("users.id"), index=True)
    project_manager = relationship("User", foreign_keys=[project_manager_id], back_populates="managed_projects")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    milestones = relationship("Milestone", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    documents = relationship("Document", back_populates="project")

class TemplateProject(Base):
    __tablename__ = "template_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    project_type = Column(Enum(ProjectType))
    region = Column(String)
    size_band_min = Column(Float)  # Minimum capacity in MW
    size_band_max = Column(Float)  # Maximum capacity in MW
    
    # Template configuration
    config = Column(JSON)  # Store template configuration as JSON
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    template_milestones = relationship("TemplateMilestone", back_populates="template_project")
    template_tasks = relationship("TemplateTask", back_populates="template_project")

class TemplateMilestone(Base):
    __tablename__ = "template_milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    order = Column(Integer)  # Order in the project lifecycle
    estimated_days = Column(Integer)  # Estimated days to complete
    
    # Relationships
    template_project_id = Column(Integer, ForeignKey("template_projects.id"), index=True)
    template_project = relationship("TemplateProject", back_populates="template_milestones")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class TemplateTask(Base):
    __tablename__ = "template_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    task_type = Column(String)  # e.g., "feasibility", "permitting", "design"
    priority = Column(String, default="medium")
    estimated_hours = Column(Float)
    
    # Relationships
    template_project_id = Column(Integer, ForeignKey("template_projects.id"), index=True)
    template_project = relationship("TemplateProject", back_populates="template_tasks")
    
    template_milestone_id = Column(Integer, ForeignKey("template_milestones.id"), nullable=True)
    template_milestone = relationship("TemplateMilestone")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

class ApprovalRule(Base):
    __tablename__ = "approval_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    
    # Rule conditions
    project_type = Column(Enum(ProjectType), nullable=True)
    region = Column(String, nullable=True)
    size_band_min = Column(Float, nullable=True)
    size_band_max = Column(Float, nullable=True)
    
    # Required approvals
    required_approvers = Column(JSON)  # List of user types or specific users
    approval_type = Column(String)  # e.g., "feasibility", "proposal", "milestone"
    
    # Rule configuration
    is_active = Column(Boolean, default=True)
    config = Column(JSON)  # Additional rule configuration
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
