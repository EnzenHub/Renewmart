# RenewMart API - Complete Documentation

## 🚀 **API Overview**

The RenewMart API is a comprehensive REST API built with FastAPI that manages the complete land development workflow from origination to Ready-to-Build (RTB). The API follows RESTful conventions and provides 80+ endpoints across 11 main modules.

**Base URL**: `http://localhost:8000`  
**API Version**: `v1`  
**API Prefix**: `/api/v1`

---

## 📋 **Table of Contents**

1. [Authentication & Authorization](#authentication--authorization)
2. [User Management](#user-management)
3. [Land Parcel Management](#land-parcel-management)
4. [Task Management](#task-management)
5. [Document Management](#document-management)
6. [Approval Workflow](#approval-workflow)
7. [Investment Opportunities](#investment-opportunities)
8. [Investment Proposals](#investment-proposals)
9. [Development Projects](#development-projects)
10. [Configuration Management](#configuration-management)
11. [Notification System](#notification-system)
12. [Testing & Validation](#testing--validation)

---

## 🔐 **Authentication & Authorization**

### **Base Route**: `/api/v1/auth`

All endpoints require JWT authentication except login. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### **POST** `/api/v1/auth/login`
**Purpose**: Authenticate user and return JWT token

**Input**:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Expected Output**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "user_type": "admin",
    "is_active": true,
    "phone": "+1234567890",
    "company": "RenewMart Inc"
  }
}
```

**Test with cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@renewmart.com&password=admin123"
```

### **POST** `/api/v1/auth/refresh`
**Purpose**: Refresh expired JWT token

**Input**: None (uses current token from Authorization header)

**Expected Output**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Test with cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer <your_token>"
```

### **POST** `/api/v1/auth/logout`
**Purpose**: Logout user (client-side token invalidation)

**Input**: None

**Expected Output**:
```json
{
  "message": "Successfully logged out"
}
```

---

## 👥 **User Management**

### **Base Route**: `/api/v1/users`

### **GET** `/api/v1/users/`
**Purpose**: List all users with optional filtering

**Query Parameters**:
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)
- `user_type` (string, optional): Filter by user type

**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "user_type": "admin",
    "is_active": true,
    "phone": "+1234567890",
    "company": "RenewMart Inc",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

**Test with cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/users/?limit=10&user_type=admin" \
  -H "Authorization: Bearer <your_token>"
```

### **GET** `/api/v1/users/{user_id}`
**Purpose**: Get specific user by ID

**Path Parameters**:
- `user_id` (int): User ID

**Expected Output**:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "user_type": "admin",
  "is_active": true,
  "phone": "+1234567890",
  "company": "RenewMart Inc",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### **POST** `/api/v1/users/`
**Purpose**: Create new user (Admin only)

**Input**:
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "securepassword123",
  "user_type": "landowner",
  "phone": "+1234567891",
  "company": "Smith Properties",
  "is_active": true
}
```

**Expected Output**:
```json
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@example.com",
  "user_type": "landowner",
  "is_active": true,
  "phone": "+1234567891",
  "company": "Smith Properties",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### **PUT** `/api/v1/users/{user_id}`
**Purpose**: Update user information

**Input**:
```json
{
  "name": "Jane Smith Updated",
  "phone": "+1234567892",
  "company": "Smith Properties LLC"
}
```

### **DELETE** `/api/v1/users/{user_id}`
**Purpose**: Delete user (Admin only)

**Expected Output**:
```json
{
  "message": "User deleted successfully"
}
```

---

## 🏞️ **Land Parcel Management**

### **Base Route**: `/api/v1/land-parcels`

### **GET** `/api/v1/land-parcels/`
**Purpose**: List all land parcels with filtering

**Query Parameters**:
- `skip`, `limit`: Pagination
- `status`: Filter by parcel status
- `landowner_id`: Filter by landowner

**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "Downtown Commercial Lot",
    "address": "123 Main St, Downtown",
    "size_acres": 2.5,
    "coordinates": {"lat": 40.7128, "lng": -74.0060},
    "description": "Prime commercial location",
    "status": "registered",
    "landowner_id": 1,
    "feasibility_completed": false,
    "feasibility_score": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/land-parcels/{parcel_id}`
**Purpose**: Get specific land parcel

### **POST** `/api/v1/land-parcels/`
**Purpose**: Create new land parcel

**Input**:
```json
{
  "name": "Industrial Zone A",
  "address": "789 Industrial Blvd",
  "size_acres": 10.0,
  "coordinates": {"lat": 40.6892, "lng": -74.0445},
  "description": "Large industrial development site",
  "landowner_id": 1
}
```

### **PUT** `/api/v1/land-parcels/{parcel_id}`
**Purpose**: Update land parcel

### **DELETE** `/api/v1/land-parcels/{parcel_id}`
**Purpose**: Delete land parcel

### **POST** `/api/v1/land-parcels/{parcel_id}/feasibility`
**Purpose**: Assign feasibility study to parcel

**Input**:
```json
{
  "analyst_id": 3,
  "due_date": "2024-02-15T17:00:00Z"
}
```

### **POST** `/api/v1/land-parcels/{parcel_id}/state/transitions`
**Purpose**: Update parcel status with validation

**Input**:
```json
{
  "new_status": "feasibility_assigned",
  "comments": "Assigned to analyst for feasibility study"
}
```

---

## 📋 **Task Management**

### **Base Route**: `/api/v1/tasks`

### **GET** `/api/v1/tasks/`
**Purpose**: List all tasks with filtering

**Query Parameters**:
- `status`: Filter by task status
- `assignee_id`: Filter by assigned user
- `skip`, `limit`: Pagination

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Feasibility Study",
    "description": "Conduct comprehensive feasibility study",
    "status": "assigned",
    "priority": "high",
    "assigned_to": 3,
    "due_date": "2024-02-15T17:00:00Z",
    "completed_at": null,
    "land_parcel_id": 1,
    "project_id": null,
    "created_by": 2,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/tasks/{task_id}`
**Purpose**: Get specific task

### **POST** `/api/v1/tasks/`
**Purpose**: Create new task

**Input**:
```json
{
  "title": "Environmental Impact Assessment",
  "description": "Complete EIA for solar project",
  "priority": "high",
  "assigned_to": 3,
  "due_date": "2024-02-20T17:00:00Z",
  "land_parcel_id": 1
}
```

### **PUT** `/api/v1/tasks/{task_id}`
**Purpose**: Update task

### **PATCH** `/api/v1/tasks/{task_id}/assign`
**Purpose**: Assign task to user

**Input**:
```json
{
  "assignee_id": 3
}
```

### **PATCH** `/api/v1/tasks/{task_id}/accept`
**Purpose**: Accept task assignment

### **PATCH** `/api/v1/tasks/{task_id}/complete`
**Purpose**: Mark task as completed

**Input**:
```json
{
  "completion_notes": "Task completed successfully with all deliverables"
}
```

### **PATCH** `/api/v1/tasks/{task_id}/reject`
**Purpose**: Reject task assignment

**Input**:
```json
{
  "rejection_reason": "Insufficient resources available"
}
```

### **GET** `/api/v1/tasks/assignee/{user_id}`
**Purpose**: Get tasks assigned to specific user

### **DELETE** `/api/v1/tasks/{task_id}`
**Purpose**: Delete task

---

## 📄 **Document Management**

### **Base Route**: `/api/v1/documents`

### **GET** `/api/v1/documents/`
**Purpose**: List all documents with filtering

**Query Parameters**:
- `document_type`: Filter by document type
- `land_parcel_id`: Filter by land parcel
- `task_id`: Filter by task
- `project_id`: Filter by project
- `proposal_id`: Filter by proposal

**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "feasibility_report.pdf",
    "file_path": "uploads/20240115_103000_feasibility_report.pdf",
    "file_size": 2048576,
    "mime_type": "application/pdf",
    "document_type": "feasibility_report",
    "checksum": "sha256:abc123...",
    "land_parcel_id": 1,
    "task_id": 1,
    "created_by": 3,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/documents/{document_id}`
**Purpose**: Get specific document metadata

### **POST** `/api/v1/documents/upload`
**Purpose**: Upload new document

**Input** (multipart/form-data):
- `file`: The file to upload
- `document_type`: Type of document
- `land_parcel_id`: Associated land parcel (optional)
- `task_id`: Associated task (optional)
- `project_id`: Associated project (optional)
- `proposal_id`: Associated proposal (optional)

**Expected Output**:
```json
{
  "message": "Document uploaded successfully",
  "document": {
    "id": 1,
    "name": "feasibility_report.pdf",
    "file_path": "uploads/20240115_103000_feasibility_report.pdf",
    "file_size": 2048576,
    "mime_type": "application/pdf",
    "document_type": "feasibility_report",
    "checksum": "sha256:abc123...",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Test with cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@/path/to/document.pdf" \
  -F "document_type=feasibility_report" \
  -F "land_parcel_id=1"
```

### **GET** `/api/v1/documents/{document_id}/download`
**Purpose**: Download document

**Expected Output**:
```json
{
  "file_path": "uploads/20240115_103000_feasibility_report.pdf",
  "filename": "feasibility_report.pdf",
  "mime_type": "application/pdf"
}
```

### **PUT** `/api/v1/documents/{document_id}`
**Purpose**: Update document metadata

### **DELETE** `/api/v1/documents/{document_id}`
**Purpose**: Delete document

### **GET** `/api/v1/documents/verify/{document_id}`
**Purpose**: Verify document integrity using checksum

**Expected Output**:
```json
{
  "document_id": 1,
  "integrity_check": "passed",
  "stored_checksum": "sha256:abc123...",
  "current_checksum": "sha256:abc123...",
  "is_valid": true
}
```

---

## ✅ **Approval Workflow**

### **Base Route**: `/api/v1/approvals`

### **GET** `/api/v1/approvals/`
**Purpose**: List all approvals with filtering

**Query Parameters**:
- `status`: Filter by approval status
- `approval_type`: Filter by approval type

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Feasibility Study Approval",
    "description": "Approve feasibility study results",
    "approval_type": "feasibility",
    "status": "pending",
    "land_parcel_id": 1,
    "project_id": null,
    "proposal_id": null,
    "created_by": 2,
    "approved_by": null,
    "approved_at": null,
    "comments": null,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/approvals/pending`
**Purpose**: Get all pending approvals

### **GET** `/api/v1/approvals/{approval_id}`
**Purpose**: Get specific approval

### **POST** `/api/v1/approvals/`
**Purpose**: Create new approval request

**Input**:
```json
{
  "title": "Project Milestone Approval",
  "description": "Approve project milestone completion",
  "approval_type": "milestone",
  "project_id": 1,
  "land_parcel_id": null,
  "proposal_id": null
}
```

### **POST** `/api/v1/approvals/{approval_id}/decision`
**Purpose**: Make approval decision (Governance only)

**Input**:
```json
{
  "decision": "approve",
  "comments": "All requirements met, approved for next phase"
}
```

**Expected Output**:
```json
{
  "message": "Approval approved successfully",
  "approval": {
    "id": 1,
    "status": "approved",
    "approved_by": 5,
    "approved_at": "2024-01-15T11:00:00Z",
    "comments": "All requirements met, approved for next phase"
  }
}
```

### **PUT** `/api/v1/approvals/{approval_id}`
**Purpose**: Update approval

### **PATCH** `/api/v1/approvals/{approval_id}/cancel`
**Purpose**: Cancel pending approval

**Input**:
```json
{
  "reason": "Requirements changed, need to resubmit"
}
```

### **DELETE** `/api/v1/approvals/{approval_id}`
**Purpose**: Delete approval

---

## 💰 **Investment Opportunities**

### **Base Route**: `/api/v1/opportunities`

### **GET** `/api/v1/opportunities/`
**Purpose**: List all investment opportunities

**Query Parameters**:
- `status`: Filter by opportunity status
- `investor_id`: Filter by investor
- `advisor_id`: Filter by advisor
- `region`: Filter by region

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Solar Farm Development Opportunity",
    "description": "Large-scale solar farm development in Texas",
    "target_capacity_mw": 100.0,
    "target_region": "Texas",
    "investment_amount": 50000000.0,
    "expected_roi": 12.5,
    "status": "submitted",
    "investor_id": 2,
    "advisor_id": 3,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/opportunities/{opportunity_id}`
**Purpose**: Get specific opportunity

### **POST** `/api/v1/opportunities/`
**Purpose**: Create new opportunity (Advisor only)

**Input**:
```json
{
  "title": "Wind Farm Development",
  "description": "Offshore wind farm development opportunity",
  "target_capacity_mw": 200.0,
  "target_region": "California",
  "investment_amount": 80000000.0,
  "expected_roi": 15.0,
  "investor_id": 2
}
```

### **PUT** `/api/v1/opportunities/{opportunity_id}`
**Purpose**: Update opportunity

### **PATCH** `/api/v1/opportunities/{opportunity_id}/state`
**Purpose**: Update opportunity status

**Input**:
```json
{
  "new_status": "under_review",
  "comments": "Moving to review phase"
}
```

### **DELETE** `/api/v1/opportunities/{opportunity_id}`
**Purpose**: Delete opportunity

### **GET** `/api/v1/opportunities/investor/{investor_id}`
**Purpose**: Get opportunities for specific investor

### **GET** `/api/v1/opportunities/advisor/{advisor_id}`
**Purpose**: Get opportunities created by specific advisor

### **GET** `/api/v1/opportunities/region/{region}`
**Purpose**: Get opportunities by region

---

## 📋 **Investment Proposals**

### **Base Route**: `/api/v1/proposals`

### **GET** `/api/v1/proposals/`
**Purpose**: List all investment proposals

**Query Parameters**:
- `status`: Filter by proposal status
- `opportunity_id`: Filter by opportunity
- `advisor_id`: Filter by advisor

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Solar Farm Proposal - Texas",
    "description": "Comprehensive proposal for 100MW solar farm",
    "total_investment": 50000000.0,
    "expected_roi": 12.5,
    "payback_period_years": 8.0,
    "status": "under_review",
    "opportunity_id": 1,
    "advisor_id": 3,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/proposals/{proposal_id}`
**Purpose**: Get specific proposal

### **POST** `/api/v1/proposals/`
**Purpose**: Create new proposal

### **POST** `/api/v1/opportunities/{opportunity_id}/proposals`
**Purpose**: Create proposal for specific opportunity

**Input**:
```json
{
  "title": "Solar Farm Proposal - Texas",
  "description": "Comprehensive proposal for 100MW solar farm",
  "total_investment": 50000000.0,
  "expected_roi": 12.5,
  "payback_period_years": 8.0
}
```

### **PUT** `/api/v1/proposals/{proposal_id}`
**Purpose**: Update proposal

### **POST** `/api/v1/proposals/{proposal_id}/approve`
**Purpose**: Approve proposal (Investor/Governance only)

**Input**:
```json
{
  "comments": "Proposal meets all requirements and investment criteria"
}
```

### **POST** `/api/v1/proposals/{proposal_id}/reject`
**Purpose**: Reject proposal

**Input**:
```json
{
  "rejection_reason": "ROI projections are too optimistic"
}
```

### **POST** `/api/v1/proposals/{proposal_id}/agreements`
**Purpose**: Create Development Service Agreement

**Input**:
```json
{
  "agreement_content": "Development Service Agreement terms and conditions..."
}
```

### **GET** `/api/v1/proposals/{proposal_id}/parcels`
**Purpose**: Get parcels associated with proposal

### **POST** `/api/v1/proposals/{proposal_id}/parcels`
**Purpose**: Add parcel to proposal

**Input**:
```json
{
  "land_parcel_id": 1,
  "allocation_percentage": 100.0
}
```

### **DELETE** `/api/v1/proposals/{proposal_id}`
**Purpose**: Delete proposal

---

## 🏗️ **Development Projects**

### **Base Route**: `/api/v1/projects`

### **GET** `/api/v1/projects/`
**Purpose**: List all development projects

**Query Parameters**:
- `status`: Filter by project status
- `project_type`: Filter by project type
- `project_manager_id`: Filter by project manager

**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "Solar Farm Development - Texas",
    "description": "100MW solar farm development project",
    "project_type": "solar",
    "status": "in_progress",
    "start_date": "2024-01-15T00:00:00Z",
    "target_completion_date": "2024-12-31T00:00:00Z",
    "actual_completion_date": null,
    "budget": 50000000.0,
    "proposal_id": 1,
    "project_manager_id": 4,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/projects/{project_id}`
**Purpose**: Get specific project

### **POST** `/api/v1/projects/`
**Purpose**: Create new project

### **POST** `/api/v1/proposals/{proposal_id}/projects`
**Purpose**: Create project from approved proposal

**Input**:
```json
{
  "name": "Solar Farm Development - Texas",
  "description": "100MW solar farm development project",
  "project_type": "solar",
  "start_date": "2024-01-15T00:00:00Z",
  "target_completion_date": "2024-12-31T00:00:00Z",
  "budget": 50000000.0,
  "project_manager_id": 4
}
```

### **PUT** `/api/v1/projects/{project_id}`
**Purpose**: Update project

### **PATCH** `/api/v1/projects/{project_id}/status`
**Purpose**: Update project status

**Input**:
```json
{
  "new_status": "stage_gate",
  "comments": "Ready for stage gate review"
}
```

### **GET** `/api/v1/projects/{project_id}/milestones`
**Purpose**: Get project milestones

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "Site Assessment",
    "description": "Complete site assessment and feasibility study",
    "order": 1,
    "status": "completed",
    "target_date": "2024-02-15T00:00:00Z",
    "actual_date": "2024-02-10T00:00:00Z",
    "project_id": 1,
    "created_by": 4,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **POST** `/api/v1/projects/{project_id}/milestones`
**Purpose**: Create project milestone

### **POST** `/api/v1/projects/{project_id}/milestones/{milestone_id}/submit`
**Purpose**: Submit milestone for approval

**Input**:
```json
{
  "submission_notes": "Milestone completed with all deliverables"
}
```

### **GET** `/api/v1/projects/{project_id}/tasks`
**Purpose**: Get project tasks

### **POST** `/api/v1/projects/{project_id}/tasks/assign`
**Purpose**: Assign task to project

### **DELETE** `/api/v1/projects/{project_id}`
**Purpose**: Delete project

---

## ⚙️ **Configuration Management**

### **Base Route**: `/api/v1/config`

### **GET** `/api/v1/config/project-types`
**Purpose**: Get project type templates

**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "Solar Farm Template",
    "project_type": "solar",
    "region": "Texas",
    "size_band": "large",
    "description": "Template for large solar farm projects",
    "is_active": true,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **POST** `/api/v1/config/project-types`
**Purpose**: Create project type template (Admin only)

**Input**:
```json
{
  "name": "Wind Farm Template",
  "project_type": "wind",
  "region": "California",
  "size_band": "medium",
  "description": "Template for medium wind farm projects"
}
```

### **PUT** `/api/v1/config/project-types/{template_id}`
**Purpose**: Update project type template

### **GET** `/api/v1/config/templates`
**Purpose**: Get task templates

### **POST** `/api/v1/config/templates`
**Purpose**: Create task template

**Input**:
```json
{
  "name": "Environmental Impact Assessment",
  "task_type": "environmental",
  "description": "Complete environmental impact assessment",
  "estimated_days": 30,
  "template_project_id": 1
}
```

### **GET** `/api/v1/config/approval-rules`
**Purpose**: Get approval rules

### **POST** `/api/v1/config/approval-rules`
**Purpose**: Create approval rule

**Input**:
```json
{
  "name": "Large Project Approval",
  "project_type": "solar",
  "region": "Texas",
  "size_band": "large",
  "required_approvals": ["governance", "finance"],
  "is_active": true
}
```

### **GET** `/api/v1/config/notification-templates`
**Purpose**: Get notification templates

### **POST** `/api/v1/config/notification-templates`
**Purpose**: Create notification template

**Input**:
```json
{
  "name": "Task Assignment Notification",
  "notification_type": "task_assignment",
  "channel": "email",
  "subject": "New Task Assigned",
  "template": "You have been assigned a new task: {{task_title}}",
  "is_active": true
}
```

### **GET** `/api/v1/config/system/health`
**Purpose**: Get system health status (Admin only)

**Expected Output**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "statistics": {
    "total_users": 25,
    "total_projects": 15,
    "total_tasks": 120,
    "total_approvals": 45
  }
}
```

---

## 🔔 **Notification System**

### **Base Route**: `/api/v1/notifications`

### **GET** `/api/v1/notifications/`
**Purpose**: Get user notifications

**Query Parameters**:
- `status`: Filter by notification status
- `notification_type`: Filter by type
- `channel`: Filter by channel

**Expected Output**:
```json
[
  {
    "id": 1,
    "title": "New Task Assigned",
    "message": "You have been assigned a new task: Feasibility Study",
    "notification_type": "task_assignment",
    "channel": "email",
    "status": "delivered",
    "user_id": 3,
    "data": {"task_id": 1},
    "read_at": null,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### **GET** `/api/v1/notifications/unread`
**Purpose**: Get unread notifications

### **GET** `/api/v1/notifications/{notification_id}`
**Purpose**: Get specific notification

### **POST** `/api/v1/notifications/`
**Purpose**: Create notification (Admin only)

### **PATCH** `/api/v1/notifications/{notification_id}/read`
**Purpose**: Mark notification as read

### **PATCH** `/api/v1/notifications/{notification_id}/unread`
**Purpose**: Mark notification as unread

### **PATCH** `/api/v1/notifications/read-all`
**Purpose**: Mark all notifications as read

### **DELETE** `/api/v1/notifications/{notification_id}`
**Purpose**: Delete notification

### **DELETE** `/api/v1/notifications/`
**Purpose**: Delete all user notifications

### **GET** `/api/v1/notifications/stats/summary`
**Purpose**: Get notification statistics

**Expected Output**:
```json
{
  "total_notifications": 25,
  "unread_notifications": 5,
  "read_notifications": 20,
  "by_type": {
    "task_assignment": 10,
    "approval_request": 8,
    "milestone_completion": 7
  }
}
```

### **POST** `/api/v1/notifications/send/bulk`
**Purpose**: Send bulk notifications (Admin only)

**Input**:
```json
{
  "user_ids": [1, 2, 3],
  "notification_type": "system_announcement",
  "channel": "email",
  "title": "System Maintenance",
  "message": "Scheduled maintenance on Sunday",
  "data": {"maintenance_time": "2024-01-21T02:00:00Z"}
}
```

### **POST** `/api/v1/notifications/send/user/{user_id}`
**Purpose**: Send notification to specific user

---

## 🧪 **Testing & Validation**

### **Health Check Endpoints**

### **GET** `/health`
**Purpose**: Basic health check

**Expected Output**:
```json
{
  "status": "healthy",
  "service": "RenewMart API"
}
```

### **GET** `/api/v1/health`
**Purpose**: API health check

**Expected Output**:
```json
{
  "status": "healthy",
  "service": "RenewMart API",
  "version": "1.0.0"
}
```

### **API Documentation**

### **GET** `/docs`
**Purpose**: Interactive API documentation (Swagger UI)

### **GET** `/redoc`
**Purpose**: Alternative API documentation (ReDoc)

---

## 🔧 **Testing Commands**

### **1. Start the Backend Server**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Test Authentication**
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@renewmart.com&password=admin123"

# Use the returned token for subsequent requests
export TOKEN="your_jwt_token_here"
```

### **3. Test User Management**
```bash
# Get all users
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"

# Create user
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "user_type": "landowner"
  }'
```

### **4. Test Land Parcel Management**
```bash
# Get all parcels
curl -X GET "http://localhost:8000/api/v1/land-parcels/" \
  -H "Authorization: Bearer $TOKEN"

# Create parcel
curl -X POST "http://localhost:8000/api/v1/land-parcels/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Parcel",
    "address": "123 Test St",
    "size_acres": 5.0,
    "coordinates": {"lat": 40.7128, "lng": -74.0060},
    "landowner_id": 1
  }'
```

### **5. Test Document Upload**
```bash
# Upload document
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/document.pdf" \
  -F "document_type=feasibility_report" \
  -F "land_parcel_id=1"
```

### **6. Test Task Management**
```bash
# Get all tasks
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Task",
    "description": "Test task description",
    "priority": "high",
    "assigned_to": 1,
    "land_parcel_id": 1
  }'
```

### **7. Test Approval Workflow**
```bash
# Get pending approvals
curl -X GET "http://localhost:8000/api/v1/approvals/pending" \
  -H "Authorization: Bearer $TOKEN"

# Make approval decision
curl -X POST "http://localhost:8000/api/v1/approvals/1/decision" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approve",
    "comments": "Approved for next phase"
  }'
```

---

## 📊 **Error Handling**

### **Common HTTP Status Codes**

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

### **Error Response Format**
```json
{
  "detail": "Error message description",
  "status_code": 400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Validation Error Format**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 🔐 **Security & Permissions**

### **User Types & Permissions**

1. **Admin**: Full access to all endpoints
2. **Governance**: Approval decisions, system oversight
3. **Project Manager**: Project management, task assignment
4. **Advisor**: Opportunity/proposal creation, stakeholder coordination
5. **Analyst**: Task execution, document upload
6. **Investor**: Proposal review, approval
7. **Landowner**: Parcel registration, status updates

### **Authentication Flow**
1. User logs in with email/password
2. Server validates credentials
3. JWT token returned with user info
4. Token included in Authorization header for subsequent requests
5. Token expires after 30 minutes (configurable)

---

## 📈 **Performance & Monitoring**

### **Database Connection**
- **Engine**: PostgreSQL with connection pooling
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic for schema management

### **API Performance**
- **Response Time**: < 200ms for most endpoints
- **Concurrent Users**: Supports 100+ concurrent requests
- **Rate Limiting**: Configurable per endpoint

### **Monitoring Endpoints**
- `/health`: Basic health check
- `/api/v1/health`: Detailed API health
- `/api/v1/config/system/health`: System statistics

---

This comprehensive API documentation covers all 80+ endpoints in the RenewMart system. Each endpoint includes detailed input/output examples, testing commands, and proper error handling. The API is designed to support the complete land development workflow from origination to Ready-to-Build (RTB).
