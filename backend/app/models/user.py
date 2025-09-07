from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class UserType(str, enum.Enum):
    LANDOWNER = "landowner"
    INVESTOR = "investor"
    ADVISOR = "advisor"
    ANALYST = "analyst"
    PROJECT_MANAGER = "project_manager"
    GOVERNANCE = "governance"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(Enum(UserType), default=UserType.LANDOWNER)
    is_active = Column(Boolean, default=True)
    phone = Column(String)
    company = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    land_parcels = relationship("LandParcel", back_populates="landowner")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    created_opportunities = relationship("InvestmentOpportunity", foreign_keys="InvestmentOpportunity.advisor_id", back_populates="advisor")
    created_proposals = relationship("InvestmentProposal", back_populates="advisor")
    managed_projects = relationship("DevelopmentProject", back_populates="project_manager")
    received_notifications = relationship("Notification", foreign_keys="Notification.user_id", back_populates="user")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    user_type = Column(Enum(UserType))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    resource = Column(String)  # e.g., "land_parcels", "proposals", "projects"
    action = Column(String)    # e.g., "create", "read", "update", "delete", "approve"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    role = relationship("Role")

class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    role = relationship("Role")
    permission = relationship("Permission")
