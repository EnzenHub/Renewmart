# Import all schemas
from .user import (
    User, UserCreate, UserUpdate,
    Role, RoleCreate, RoleUpdate,
    Permission, PermissionCreate, PermissionUpdate,
    UserRole, UserRoleCreate,
    RolePermission, RolePermissionCreate
)
from .land_parcel import (
    LandParcel, LandParcelCreate, LandParcelUpdate,
    Document, DocumentCreate, DocumentUpdate,
    Task, TaskCreate, TaskUpdate,
    Approval, ApprovalCreate, ApprovalUpdate,
    Milestone, MilestoneCreate, MilestoneUpdate,
    Coordinates
)
from .investment import (
    InvestmentOpportunity, InvestmentOpportunityCreate, InvestmentOpportunityUpdate,
    InvestmentProposal, InvestmentProposalCreate, InvestmentProposalUpdate,
    ProposalParcel, ProposalParcelCreate, ProposalParcelUpdate
)
from .project import (
    DevelopmentProject, DevelopmentProjectCreate, DevelopmentProjectUpdate,
    TemplateProject, TemplateProjectCreate, TemplateProjectUpdate,
    TemplateMilestone, TemplateMilestoneCreate, TemplateMilestoneUpdate,
    TemplateTask, TemplateTaskCreate, TemplateTaskUpdate,
    ApprovalRule, ApprovalRuleCreate, ApprovalRuleUpdate
)
from .notification import (
    Notification, NotificationCreate, NotificationUpdate,
    NotificationTemplate, NotificationTemplateCreate, NotificationTemplateUpdate
)

__all__ = [
    # User schemas
    "User", "UserCreate", "UserUpdate",
    "Role", "RoleCreate", "RoleUpdate",
    "Permission", "PermissionCreate", "PermissionUpdate",
    "UserRole", "UserRoleCreate",
    "RolePermission", "RolePermissionCreate",
    
    # Land parcel schemas
    "LandParcel", "LandParcelCreate", "LandParcelUpdate",
    "Document", "DocumentCreate", "DocumentUpdate",
    "Task", "TaskCreate", "TaskUpdate",
    "Approval", "ApprovalCreate", "ApprovalUpdate",
    "Milestone", "MilestoneCreate", "MilestoneUpdate",
    "Coordinates",
    
    # Investment schemas
    "InvestmentOpportunity", "InvestmentOpportunityCreate", "InvestmentOpportunityUpdate",
    "InvestmentProposal", "InvestmentProposalCreate", "InvestmentProposalUpdate",
    "ProposalParcel", "ProposalParcelCreate", "ProposalParcelUpdate",
    
    # Project schemas
    "DevelopmentProject", "DevelopmentProjectCreate", "DevelopmentProjectUpdate",
    "TemplateProject", "TemplateProjectCreate", "TemplateProjectUpdate",
    "TemplateMilestone", "TemplateMilestoneCreate", "TemplateMilestoneUpdate",
    "TemplateTask", "TemplateTaskCreate", "TemplateTaskUpdate",
    "ApprovalRule", "ApprovalRuleCreate", "ApprovalRuleUpdate",
    
    # Notification schemas
    "Notification", "NotificationCreate", "NotificationUpdate",
    "NotificationTemplate", "NotificationTemplateCreate", "NotificationTemplateUpdate",
]
