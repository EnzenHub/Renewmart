from fastapi import APIRouter
from app.api.endpoints import (
    users, land_parcels, auth, tasks, documents, approvals,
    opportunities, proposals, projects, config, notifications
)

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(land_parcels.router, prefix="/land-parcels", tags=["land-parcels"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["investment-opportunities"])
api_router.include_router(proposals.router, prefix="/proposals", tags=["investment-proposals"])
api_router.include_router(projects.router, prefix="/projects", tags=["development-projects"])
api_router.include_router(config.router, prefix="/config", tags=["configuration"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
