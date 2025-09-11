# Import all models to ensure they are registered with SQLAlchemy
from .user import User, Role, Permission, UserRole, RolePermission, UserType
from .land_parcel import (
    LandParcel, Document, Task, Approval, Milestone,
    ParcelStatus, TaskStatus, ApprovalStatus, MilestoneStatus
)
from .investment import (
    InvestmentOpportunity, InvestmentProposal, ProposalParcel,
    OpportunityStatus, ProposalStatus
)
from .project import (
    DevelopmentProject, TemplateProject, TemplateMilestone, TemplateTask, ApprovalRule,
    ProjectStatus, ProjectType
)
from .notification import (
    Notification, NotificationTemplate,
    NotificationType, NotificationChannel, NotificationStatus
)

__all__ = [
    # User models
    "User", "Role", "Permission", "UserRole", "RolePermission", "UserType",
    
    # Land parcel models
    "LandParcel", "Document", "Task", "Approval", "Milestone",
    "ParcelStatus", "TaskStatus", "ApprovalStatus", "MilestoneStatus",
    
    # Investment models
    "InvestmentOpportunity", "InvestmentProposal", "ProposalParcel",
    "OpportunityStatus", "ProposalStatus",
    
    # Project models
    "DevelopmentProject", "TemplateProject", "TemplateMilestone", "TemplateTask", "ApprovalRule",
    "ProjectStatus", "ProjectType",
    
    # Notification models
    "Notification", "NotificationTemplate",
    "NotificationType", "NotificationChannel", "NotificationStatus",
]
