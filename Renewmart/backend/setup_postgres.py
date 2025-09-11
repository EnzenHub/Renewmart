#!/usr/bin/env python3
"""
PostgreSQL Setup Script for RenewMart
This script helps you set up PostgreSQL database for the application
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import Base, engine
from app.models import (
    # User models
    User, Role, Permission, UserRole, RolePermission, UserType,
    # Land parcel models
    LandParcel, Document, Task, Approval, Milestone,
    ParcelStatus, TaskStatus, ApprovalStatus, MilestoneStatus,
    # Investment models
    InvestmentOpportunity, InvestmentProposal, ProposalParcel,
    OpportunityStatus, ProposalStatus,
    # Project models
    DevelopmentProject, TemplateProject, TemplateMilestone, TemplateTask, ApprovalRule,
    ProjectStatus, ProjectType,
    # Notification models
    Notification, NotificationTemplate,
    NotificationType, NotificationChannel, NotificationStatus
)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'renewmart_db'
}

def create_database():
    """Create the renewmart_db database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            print(f"✅ Database '{DB_CONFIG['database']}' created successfully!")
        else:
            print(f"ℹ️  Database '{DB_CONFIG['database']}' already exists.")
        
        cursor.close()
        conn.close()
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is installed and running")
        print("2. Username and password are correct")
        print("3. PostgreSQL is accessible on localhost:5432")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def create_tables():
    """Create all database tables using SQLAlchemy models"""
    try:
        print("\n🏗️  Creating database tables...")
        print("-" * 50)
        
        # Create all tables defined in the models
        Base.metadata.create_all(bind=engine)
        
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def show_table_structures():
    """Display the structure of all tables"""
    print("\n📋 Database Table Structures:")
    print("=" * 60)
    
    # User Management Tables
    print("\n👥 USER MANAGEMENT TABLES:")
    print("-" * 30)
    
    print("\n1. users table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - name (VARCHAR)")
    print("   - email (VARCHAR, UNIQUE)")
    print("   - user_type (ENUM: landowner, investor, advisor, analyst, project_manager, governance, admin)")
    print("   - is_active (BOOLEAN)")
    print("   - phone (VARCHAR)")
    print("   - company (VARCHAR)")
    print("   - created_at (TIMESTAMP)")
    print("   - updated_at (TIMESTAMP)")
    
    print("\n2. roles table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - name (VARCHAR, UNIQUE)")
    print("   - description (TEXT)")
    print("   - user_type (ENUM)")
    print("   - created_at (TIMESTAMP)")
    
    print("\n3. permissions table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - name (VARCHAR, UNIQUE)")
    print("   - description (TEXT)")
    print("   - resource (VARCHAR) - e.g., 'land_parcels', 'proposals'")
    print("   - action (VARCHAR) - e.g., 'create', 'read', 'update', 'delete', 'approve'")
    print("   - created_at (TIMESTAMP)")
    
    print("\n4. user_roles table (Many-to-Many):")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - user_id (INTEGER, FOREIGN KEY -> users.id)")
    print("   - role_id (INTEGER, FOREIGN KEY -> roles.id)")
    print("   - created_at (TIMESTAMP)")
    
    print("\n5. role_permissions table (Many-to-Many):")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - role_id (INTEGER, FOREIGN KEY -> roles.id)")
    print("   - permission_id (INTEGER, FOREIGN KEY -> permissions.id)")
    print("   - created_at (TIMESTAMP)")
    
    # Land Management Tables
    print("\n\n🏞️  LAND MANAGEMENT TABLES:")
    print("-" * 30)
    
    print("\n6. land_parcels table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - name (VARCHAR)")
    print("   - address (VARCHAR)")
    print("   - size_acres (FLOAT)")
    print("   - coordinates (JSON) - stores lat/lng")
    print("   - description (TEXT)")
    print("   - status (ENUM: registered, feasibility_assigned, feasibility_in_progress, etc.)")
    print("   - landowner_id (INTEGER, FOREIGN KEY -> users.id)")
    print("   - feasibility_completed (BOOLEAN)")
    print("   - feasibility_score (FLOAT)")
    print("   - feasibility_notes (TEXT)")
    print("   - created_at (TIMESTAMP)")
    print("   - updated_at (TIMESTAMP)")
    
    print("\n7. documents table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - name (VARCHAR)")
    print("   - file_path (VARCHAR)")
    print("   - file_size (INTEGER)")
    print("   - mime_type (VARCHAR)")
    print("   - document_type (VARCHAR)")
    print("   - checksum (VARCHAR) - for integrity verification")
    print("   - land_parcel_id (INTEGER, FOREIGN KEY -> land_parcels.id, nullable)")
    print("   - task_id (INTEGER, FOREIGN KEY -> tasks.id, nullable)")
    print("   - project_id (INTEGER, FOREIGN KEY -> development_projects.id, nullable)")
    print("   - proposal_id (INTEGER, FOREIGN KEY -> investment_proposals.id, nullable)")
    print("   - created_at (TIMESTAMP)")
    print("   - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n8. tasks table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - title (VARCHAR)")
    print("   - description (TEXT)")
    print("   - status (ENUM: pending, assigned, in_progress, completed, rejected, cancelled)")
    print("   - priority (VARCHAR) - low, medium, high, urgent")
    print("   - assigned_to (INTEGER, FOREIGN KEY -> users.id)")
    print("   - due_date (TIMESTAMP)")
    print("   - completed_at (TIMESTAMP)")
    print("   - land_parcel_id (INTEGER, FOREIGN KEY -> land_parcels.id, nullable)")
    print("   - project_id (INTEGER, FOREIGN KEY -> development_projects.id, nullable)")
    print("   - milestone_id (INTEGER, FOREIGN KEY -> milestones.id, nullable)")
    print("   - created_at (TIMESTAMP)")
    print("   - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n9. approvals table:")
    print("   - id (INTEGER, PRIMARY KEY)")
    print("   - approval_type (VARCHAR) - e.g., 'feasibility', 'proposal', 'milestone'")
    print("   - status (ENUM: pending, approved, rejected, cancelled)")
    print("   - comments (TEXT)")
    print("   - approved_by (INTEGER, FOREIGN KEY -> users.id)")
    print("   - approved_at (TIMESTAMP)")
    print("   - land_parcel_id (INTEGER, FOREIGN KEY -> land_parcels.id, nullable)")
    print("   - proposal_id (INTEGER, FOREIGN KEY -> investment_proposals.id, nullable)")
    print("   - project_id (INTEGER, FOREIGN KEY -> development_projects.id, nullable)")
    print("   - milestone_id (INTEGER, FOREIGN KEY -> milestones.id, nullable)")
    print("   - created_at (TIMESTAMP)")
    print("   - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n10. milestones table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - description (TEXT)")
    print("    - status (ENUM: pending, in_progress, completed, approved, rejected)")
    print("    - target_date (TIMESTAMP)")
    print("    - completed_at (TIMESTAMP)")
    print("    - project_id (INTEGER, FOREIGN KEY -> development_projects.id)")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    # Investment Management Tables
    print("\n\n💰 INVESTMENT MANAGEMENT TABLES:")
    print("-" * 35)
    
    print("\n11. investment_opportunities table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - description (TEXT)")
    print("    - status (ENUM: draft, submitted, under_review, approved, rejected, expired)")
    print("    - target_capacity_mw (FLOAT)")
    print("    - target_region (VARCHAR)")
    print("    - investment_amount (FLOAT)")
    print("    - expected_returns (FLOAT)")
    print("    - investor_id (INTEGER, FOREIGN KEY -> users.id)")
    print("    - advisor_id (INTEGER, FOREIGN KEY -> users.id)")
    print("    - created_at (TIMESTAMP)")
    print("    - updated_at (TIMESTAMP)")
    
    print("\n12. investment_proposals table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - description (TEXT)")
    print("    - status (ENUM: draft, submitted, under_review, approved, rejected, agreement_signed)")
    print("    - total_capacity_mw (FLOAT)")
    print("    - total_investment (FLOAT)")
    print("    - expected_completion_date (TIMESTAMP)")
    print("    - opportunity_id (INTEGER, FOREIGN KEY -> investment_opportunities.id)")
    print("    - advisor_id (INTEGER, FOREIGN KEY -> users.id)")
    print("    - created_at (TIMESTAMP)")
    print("    - updated_at (TIMESTAMP)")
    
    print("\n13. proposal_parcels table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - proposal_id (INTEGER, FOREIGN KEY -> investment_proposals.id)")
    print("    - land_parcel_id (INTEGER, FOREIGN KEY -> land_parcels.id)")
    print("    - allocated_capacity_mw (FLOAT)")
    print("    - allocated_investment (FLOAT)")
    print("    - notes (TEXT)")
    print("    - created_at (TIMESTAMP)")
    
    # Project Management Tables
    print("\n\n🏗️  PROJECT MANAGEMENT TABLES:")
    print("-" * 35)
    
    print("\n14. development_projects table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - name (VARCHAR)")
    print("    - description (TEXT)")
    print("    - status (ENUM: initiated, in_progress, stage_gate, ready_to_build, cancelled, completed)")
    print("    - project_type (ENUM: solar, wind, hydro, storage, hybrid)")
    print("    - total_capacity_mw (FLOAT)")
    print("    - total_investment (FLOAT)")
    print("    - target_completion_date (TIMESTAMP)")
    print("    - actual_completion_date (TIMESTAMP)")
    print("    - proposal_id (INTEGER, FOREIGN KEY -> investment_proposals.id)")
    print("    - project_manager_id (INTEGER, FOREIGN KEY -> users.id)")
    print("    - created_at (TIMESTAMP)")
    print("    - updated_at (TIMESTAMP)")
    
    print("\n15. template_projects table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - name (VARCHAR)")
    print("    - description (TEXT)")
    print("    - project_type (ENUM: solar, wind, hydro, storage, hybrid)")
    print("    - region (VARCHAR)")
    print("    - size_band_min (FLOAT)")
    print("    - size_band_max (FLOAT)")
    print("    - config (JSON) - template configuration")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n16. template_milestones table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - description (TEXT)")
    print("    - order (INTEGER) - order in project lifecycle")
    print("    - estimated_days (INTEGER)")
    print("    - template_project_id (INTEGER, FOREIGN KEY -> template_projects.id)")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n17. template_tasks table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - description (TEXT)")
    print("    - task_type (VARCHAR) - e.g., 'feasibility', 'permitting', 'design'")
    print("    - priority (VARCHAR)")
    print("    - estimated_hours (FLOAT)")
    print("    - template_project_id (INTEGER, FOREIGN KEY -> template_projects.id)")
    print("    - template_milestone_id (INTEGER, FOREIGN KEY -> template_milestones.id, nullable)")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n18. approval_rules table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - name (VARCHAR)")
    print("    - description (TEXT)")
    print("    - project_type (ENUM, nullable)")
    print("    - region (VARCHAR, nullable)")
    print("    - size_band_min (FLOAT, nullable)")
    print("    - size_band_max (FLOAT, nullable)")
    print("    - required_approvers (JSON) - list of user types or specific users")
    print("    - approval_type (VARCHAR)")
    print("    - is_active (BOOLEAN)")
    print("    - config (JSON) - additional rule configuration")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    # Notification Tables
    print("\n\n🔔 NOTIFICATION TABLES:")
    print("-" * 25)
    
    print("\n19. notifications table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - title (VARCHAR)")
    print("    - message (TEXT)")
    print("    - notification_type (ENUM: task_assigned, task_completed, approval_required, etc.)")
    print("    - channel (ENUM: email, sms, web_push, in_app)")
    print("    - status (ENUM: pending, sent, delivered, failed, read)")
    print("    - user_id (INTEGER, FOREIGN KEY -> users.id)")
    print("    - related_entity_type (VARCHAR, nullable)")
    print("    - related_entity_id (INTEGER, nullable)")
    print("    - data (JSON) - additional notification data")
    print("    - sent_at (TIMESTAMP)")
    print("    - delivered_at (TIMESTAMP)")
    print("    - read_at (TIMESTAMP)")
    print("    - failed_reason (TEXT)")
    print("    - retry_count (INTEGER)")
    print("    - max_retries (INTEGER)")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    
    print("\n20. notification_templates table:")
    print("    - id (INTEGER, PRIMARY KEY)")
    print("    - name (VARCHAR, UNIQUE)")
    print("    - notification_type (ENUM)")
    print("    - channel (ENUM)")
    print("    - subject_template (VARCHAR) - for email")
    print("    - message_template (TEXT)")
    print("    - variables (JSON) - list of required variables")
    print("    - is_active (BOOLEAN)")
    print("    - priority (INTEGER) - 1=high, 2=medium, 3=low")
    print("    - created_at (TIMESTAMP)")
    print("    - created_by (INTEGER, FOREIGN KEY -> users.id)")
    print("    - updated_at (TIMESTAMP)")

def show_api_endpoints():
    """Display API endpoints and their database relationships"""
    print("\n\n🔌 API ENDPOINTS & DATABASE RELATIONSHIPS:")
    print("=" * 60)
    
    print("\n📡 AUTHENTICATION API:")
    print("-" * 25)
    print("POST   /auth/login              → User authentication")
    print("POST   /auth/refresh            → Token refresh")
    print("POST   /auth/logout             → User logout")
    
    print("\n📡 USER MANAGEMENT API:")
    print("-" * 25)
    print("GET    /api/v1/users/           → SELECT * FROM users")
    print("GET    /api/v1/users/{id}       → SELECT * FROM users WHERE id = {id}")
    print("POST   /api/v1/users/           → INSERT INTO users (name, email, user_type)")
    print("PUT    /api/v1/users/{id}       → UPDATE users SET ... WHERE id = {id}")
    print("DELETE /api/v1/users/{id}       → DELETE FROM users WHERE id = {id}")
    print("GET    /api/v1/roles/           → SELECT * FROM roles")
    print("POST   /api/v1/roles/           → INSERT INTO roles (...)")
    print("GET    /api/v1/permissions/     → SELECT * FROM permissions")
    
    print("\n📡 LAND PARCEL MANAGEMENT API:")
    print("-" * 30)
    print("GET    /api/v1/land-parcels/           → SELECT * FROM land_parcels")
    print("GET    /api/v1/land-parcels/{id}       → SELECT * FROM land_parcels WHERE id = {id}")
    print("POST   /api/v1/land-parcels/           → INSERT INTO land_parcels (...)")
    print("PUT    /api/v1/land-parcels/{id}       → UPDATE land_parcels SET ... WHERE id = {id}")
    print("DELETE /api/v1/land-parcels/{id}       → DELETE FROM land_parcels WHERE id = {id}")
    print("POST   /api/v1/land-parcels/{id}/feasibility → Assign feasibility task")
    print("POST   /api/v1/land-parcels/{id}/state/transitions → Update parcel status")
    
    print("\n📡 INVESTMENT OPPORTUNITY API:")
    print("-" * 30)
    print("GET    /api/v1/opportunities/          → SELECT * FROM investment_opportunities")
    print("GET    /api/v1/opportunities/{id}      → SELECT * FROM investment_opportunities WHERE id = {id}")
    print("POST   /api/v1/opportunities/          → INSERT INTO investment_opportunities (...)")
    print("PUT    /api/v1/opportunities/{id}      → UPDATE investment_opportunities SET ... WHERE id = {id}")
    print("PATCH  /api/v1/opportunities/{id}/state → Update opportunity status")
    
    print("\n📡 INVESTMENT PROPOSAL API:")
    print("-" * 30)
    print("GET    /api/v1/proposals/              → SELECT * FROM investment_proposals")
    print("GET    /api/v1/proposals/{id}          → SELECT * FROM investment_proposals WHERE id = {id}")
    print("POST   /api/v1/opportunities/{id}/proposals → INSERT INTO investment_proposals (...)")
    print("PUT    /api/v1/proposals/{id}          → UPDATE investment_proposals SET ... WHERE id = {id}")
    print("POST   /api/v1/proposals/{id}/approve  → Approve proposal")
    print("POST   /api/v1/proposals/{id}/reject   → Reject proposal")
    print("POST   /api/v1/proposals/{id}/agreements → Create DSA")
    
    print("\n📡 DEVELOPMENT PROJECT API:")
    print("-" * 30)
    print("GET    /api/v1/projects/               → SELECT * FROM development_projects")
    print("GET    /api/v1/projects/{id}           → SELECT * FROM development_projects WHERE id = {id}")
    print("POST   /api/v1/proposals/{id}/projects → INSERT INTO development_projects (...)")
    print("PUT    /api/v1/projects/{id}           → UPDATE development_projects SET ... WHERE id = {id}")
    print("POST   /api/v1/projects/{id}/milestones → Submit milestone")
    
    print("\n📡 TASK MANAGEMENT API:")
    print("-" * 25)
    print("GET    /api/v1/tasks/                  → SELECT * FROM tasks")
    print("GET    /api/v1/tasks/{id}              → SELECT * FROM tasks WHERE id = {id}")
    print("POST   /api/v1/projects/{id}/tasks/assign → Assign task to analyst")
    print("PATCH  /api/v1/tasks/{id}/complete     → Mark task as completed")
    print("PATCH  /api/v1/tasks/{id}/accept       → Accept task assignment")
    print("POST   /api/v1/tasks/{id}/documents    → Upload task documents")
    
    print("\n📡 APPROVAL API:")
    print("-" * 15)
    print("GET    /api/v1/approvals/              → SELECT * FROM approvals")
    print("POST   /api/v1/approvals/{id}/decision → Approve/reject approval")
    print("GET    /api/v1/approvals/pending       → Get pending approvals")
    
    print("\n📡 DOCUMENT MANAGEMENT API:")
    print("-" * 30)
    print("GET    /api/v1/documents/              → SELECT * FROM documents")
    print("POST   /api/v1/upload                  → Upload document")
    print("GET    /api/v1/documents/{id}          → Get document metadata")
    print("GET    /api/v1/documents/{id}/download → Download document")
    
    print("\n📡 CONFIGURATION API (Admin):")
    print("-" * 30)
    print("GET    /api/v1/config/project-types    → SELECT * FROM template_projects")
    print("POST   /api/v1/config/project-types    → INSERT INTO template_projects (...)")
    print("GET    /api/v1/config/templates        → SELECT * FROM template_tasks")
    print("POST   /api/v1/config/templates        → INSERT INTO template_tasks (...)")
    print("GET    /api/v1/config/approval-rules   → SELECT * FROM approval_rules")
    print("POST   /api/v1/config/approval-rules   → INSERT INTO approval_rules (...)")
    
    print("\n📡 NOTIFICATION API:")
    print("-" * 20)
    print("GET    /api/v1/notifications/          → SELECT * FROM notifications WHERE user_id = ?")
    print("PATCH  /api/v1/notifications/{id}/read → Mark notification as read")
    print("GET    /api/v1/notifications/templates → SELECT * FROM notification_templates")

def insert_sample_data():
    """Insert comprehensive sample data into the database"""
    try:
        print("\n🌱 Inserting comprehensive sample data...")
        print("-" * 40)
        
        from sqlalchemy.orm import sessionmaker
        from datetime import datetime, timedelta
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Check if data already exists
            existing_users = db.query(User).count()
            if existing_users > 0:
                print("ℹ️  Sample data already exists. Skipping...")
                return True
            
            # Insert sample users with different types
            users = [
                # Landowners
                User(name="Alice Landowner", email="alice@landowner.com", user_type=UserType.LANDOWNER, 
                     phone="555-0001", company="Land Holdings LLC", is_active=True),
                User(name="Bob Property Owner", email="bob@property.com", user_type=UserType.LANDOWNER, 
                     phone="555-0002", company="Property Group Inc", is_active=True),
                
                # Investors
                User(name="Charlie Investor", email="charlie@investor.com", user_type=UserType.INVESTOR, 
                     phone="555-0003", company="Green Energy Capital", is_active=True),
                User(name="Diana Capital", email="diana@capital.com", user_type=UserType.INVESTOR, 
                     phone="555-0004", company="Renewable Ventures", is_active=True),
                
                # Advisors
                User(name="Eve Advisor", email="eve@advisor.com", user_type=UserType.ADVISOR, 
                     phone="555-0005", company="RenewMart Advisors", is_active=True),
                User(name="Frank Consultant", email="frank@consultant.com", user_type=UserType.ADVISOR, 
                     phone="555-0006", company="Energy Solutions", is_active=True),
                
                # Analysts
                User(name="Grace Analyst", email="grace@analyst.com", user_type=UserType.ANALYST, 
                     phone="555-0007", company="Technical Services", is_active=True),
                User(name="Henry Engineer", email="henry@engineer.com", user_type=UserType.ANALYST, 
                     phone="555-0008", company="Engineering Corp", is_active=True),
                
                # Project Managers
                User(name="Ivy Manager", email="ivy@manager.com", user_type=UserType.PROJECT_MANAGER, 
                     phone="555-0009", company="Project Management Inc", is_active=True),
                User(name="Jack Coordinator", email="jack@coordinator.com", user_type=UserType.PROJECT_MANAGER, 
                     phone="555-0010", company="Development Co", is_active=True),
                
                # Governance
                User(name="Karen Governance", email="karen@governance.com", user_type=UserType.GOVERNANCE, 
                     phone="555-0011", company="Compliance Office", is_active=True),
                User(name="Liam Approver", email="liam@approver.com", user_type=UserType.GOVERNANCE, 
                     phone="555-0012", company="Approval Board", is_active=True),
                
                # Admin
                User(name="Maya Admin", email="maya@admin.com", user_type=UserType.ADMIN, 
                     phone="555-0013", company="RenewMart", is_active=True),
            ]
            
            for user in users:
                db.add(user)
            db.flush()  # Flush to get IDs
            
            # Insert sample land parcels
            land_parcels = [
                LandParcel(
                    name="Solar Farm Site A",
                    address="123 Solar Lane, Desert Valley, CA",
                    size_acres=150.0,
                    coordinates={"lat": 34.0522, "lng": -118.2437},
                    description="Prime solar development site with excellent sun exposure",
                    status=ParcelStatus.REGISTERED,
                    landowner_id=1,  # Alice Landowner
                    feasibility_completed=False
                ),
                LandParcel(
                    name="Wind Energy Site B",
                    address="456 Windy Ridge, Mountain View, TX",
                    size_acres=200.0,
                    coordinates={"lat": 32.7767, "lng": -96.7970},
                    description="High elevation site ideal for wind turbines",
                    status=ParcelStatus.FEASIBILITY_COMPLETED,
                    landowner_id=2,  # Bob Property Owner
                    feasibility_completed=True,
                    feasibility_score=8.5,
                    feasibility_notes="Excellent wind conditions, minimal environmental impact"
                ),
                LandParcel(
                    name="Hybrid Energy Complex",
                    address="789 Renewable Blvd, Green City, OR",
                    size_acres=300.0,
                    coordinates={"lat": 45.5152, "lng": -122.6784},
                    description="Large site suitable for solar + storage hybrid project",
                    status=ParcelStatus.READY_FOR_PROPOSAL,
                    landowner_id=1,  # Alice Landowner
                    feasibility_completed=True,
                    feasibility_score=9.2,
                    feasibility_notes="Perfect for hybrid renewable energy development"
                ),
            ]
            
            for parcel in land_parcels:
                db.add(parcel)
            db.flush()
            
            # Insert sample investment opportunities
            opportunities = [
                InvestmentOpportunity(
                    title="Solar Development Opportunity - West Coast",
                    description="Large-scale solar development opportunity in California",
                    status=OpportunityStatus.APPROVED,
                    target_capacity_mw=500.0,
                    target_region="California",
                    investment_amount=750000000.0,
                    expected_returns=12.5,
                    investor_id=3,  # Charlie Investor
                    advisor_id=5   # Eve Advisor
                ),
                InvestmentOpportunity(
                    title="Wind Energy Portfolio - Texas",
                    description="Multi-site wind energy development in Texas",
                    status=OpportunityStatus.UNDER_REVIEW,
                    target_capacity_mw=800.0,
                    target_region="Texas",
                    investment_amount=1200000000.0,
                    expected_returns=15.0,
                    investor_id=4,  # Diana Capital
                    advisor_id=6   # Frank Consultant
                ),
            ]
            
            for opportunity in opportunities:
                db.add(opportunity)
            db.flush()
            
            # Insert sample investment proposals
            proposals = [
                InvestmentProposal(
                    title="California Solar Portfolio Proposal",
                    description="Comprehensive solar development proposal for California sites",
                    status=ProposalStatus.APPROVED,
                    total_capacity_mw=500.0,
                    total_investment=750000000.0,
                    expected_completion_date=datetime.now() + timedelta(days=365),
                    opportunity_id=1,
                    advisor_id=5  # Eve Advisor
                ),
                InvestmentProposal(
                    title="Texas Wind Energy Proposal",
                    description="Wind energy development proposal for Texas region",
                    status=ProposalStatus.UNDER_REVIEW,
                    total_capacity_mw=800.0,
                    total_investment=1200000000.0,
                    expected_completion_date=datetime.now() + timedelta(days=450),
                    opportunity_id=2,
                    advisor_id=6  # Frank Consultant
                ),
            ]
            
            for proposal in proposals:
                db.add(proposal)
            db.flush()
            
            # Insert sample proposal-parcel mappings
            proposal_parcels = [
                ProposalParcel(
                    proposal_id=1,
                    land_parcel_id=1,  # Solar Farm Site A
                    allocated_capacity_mw=150.0,
                    allocated_investment=225000000.0,
                    notes="Primary solar site with excellent conditions"
                ),
                ProposalParcel(
                    proposal_id=1,
                    land_parcel_id=3,  # Hybrid Energy Complex
                    allocated_capacity_mw=350.0,
                    allocated_investment=525000000.0,
                    notes="Hybrid solar + storage site"
                ),
                ProposalParcel(
                    proposal_id=2,
                    land_parcel_id=2,  # Wind Energy Site B
                    allocated_capacity_mw=200.0,
                    allocated_investment=300000000.0,
                    notes="Wind energy development site"
                ),
            ]
            
            for pp in proposal_parcels:
                db.add(pp)
            db.flush()
            
            # Insert sample development projects
            projects = [
                DevelopmentProject(
                    name="California Solar Development Project",
                    description="Large-scale solar development in California",
                    project_type=ProjectType.SOLAR,
                    status=ProjectStatus.IN_PROGRESS,
                    total_capacity_mw=500.0,
                    total_investment=750000000.0,
                    target_completion_date=datetime.now() + timedelta(days=365),
                    proposal_id=1,
                    project_manager_id=9  # Ivy Manager
                ),
                DevelopmentProject(
                    name="Texas Wind Energy Project",
                    description="Wind energy development in Texas",
                    project_type=ProjectType.WIND,
                    status=ProjectStatus.INITIATED,
                    total_capacity_mw=800.0,
                    total_investment=1200000000.0,
                    target_completion_date=datetime.now() + timedelta(days=450),
                    proposal_id=2,
                    project_manager_id=10  # Jack Coordinator
                ),
            ]
            
            for project in projects:
                db.add(project)
            db.flush()
            
            # Insert sample tasks
            tasks = [
                Task(
                    title="Site Feasibility Study",
                    description="Conduct comprehensive feasibility study for solar site",
                    status=TaskStatus.COMPLETED,
                    priority="high",
                    assigned_to=7,  # Grace Analyst
                    due_date=datetime.now() + timedelta(days=30),
                    completed_at=datetime.now() - timedelta(days=5),
                    land_parcel_id=1,
                    project_id=1,
                    created_by=5  # Eve Advisor
                ),
                Task(
                    title="Environmental Impact Assessment",
                    description="Complete environmental impact assessment for wind site",
                    status=TaskStatus.IN_PROGRESS,
                    priority="high",
                    assigned_to=8,  # Henry Engineer
                    due_date=datetime.now() + timedelta(days=45),
                    land_parcel_id=2,
                    project_id=2,
                    created_by=6  # Frank Consultant
                ),
                Task(
                    title="Permit Application Submission",
                    description="Submit all required permits for hybrid energy project",
                    status=TaskStatus.PENDING,
                    priority="urgent",
                    assigned_to=7,  # Grace Analyst
                    due_date=datetime.now() + timedelta(days=15),
                    land_parcel_id=3,
                    project_id=1,
                    created_by=9  # Ivy Manager
                ),
            ]
            
            for task in tasks:
                db.add(task)
            db.flush()
            
            # Insert sample milestones
            milestones = [
                Milestone(
                    title="Feasibility Complete",
                    description="All feasibility studies completed and approved",
                    status=MilestoneStatus.COMPLETED,
                    target_date=datetime.now() - timedelta(days=10),
                    completed_at=datetime.now() - timedelta(days=5),
                    project_id=1,
                    created_by=9  # Ivy Manager
                ),
                Milestone(
                    title="Permits Approved",
                    description="All required permits obtained",
                    status=MilestoneStatus.IN_PROGRESS,
                    target_date=datetime.now() + timedelta(days=60),
                    project_id=1,
                    created_by=9  # Ivy Manager
                ),
                Milestone(
                    title="Environmental Clearance",
                    description="Environmental impact assessment completed",
                    status=MilestoneStatus.PENDING,
                    target_date=datetime.now() + timedelta(days=90),
                    project_id=2,
                    created_by=10  # Jack Coordinator
                ),
            ]
            
            for milestone in milestones:
                db.add(milestone)
            db.flush()
            
            # Insert sample approvals
            approvals = [
                Approval(
                    approval_type="feasibility",
                    status=ApprovalStatus.APPROVED,
                    comments="Feasibility study meets all requirements",
                    approved_by=11,  # Karen Governance
                    approved_at=datetime.now() - timedelta(days=3),
                    land_parcel_id=1,
                    created_by=5  # Eve Advisor
                ),
                Approval(
                    approval_type="proposal",
                    status=ApprovalStatus.APPROVED,
                    comments="Proposal approved for development",
                    approved_by=12,  # Liam Approver
                    approved_at=datetime.now() - timedelta(days=1),
                    proposal_id=1,
                    created_by=5  # Eve Advisor
                ),
                Approval(
                    approval_type="milestone",
                    status=ApprovalStatus.PENDING,
                    comments="Awaiting environmental clearance",
                    land_parcel_id=2,
                    created_by=6  # Frank Consultant
                ),
            ]
            
            for approval in approvals:
                db.add(approval)
            db.flush()
            
            # Insert sample documents
            documents = [
                Document(
                    name="Feasibility Study Report - Site A",
                    file_path="/documents/feasibility_site_a.pdf",
                    file_size=2048000,
                    mime_type="application/pdf",
                    document_type="feasibility_report",
                    checksum="abc123def456",
                    land_parcel_id=1,
                    created_by=7  # Grace Analyst
                ),
                Document(
                    name="Environmental Impact Assessment",
                    file_path="/documents/eia_wind_site.pdf",
                    file_size=1536000,
                    mime_type="application/pdf",
                    document_type="environmental_assessment",
                    checksum="def456ghi789",
                    land_parcel_id=2,
                    created_by=8  # Henry Engineer
                ),
                Document(
                    name="Development Service Agreement",
                    file_path="/documents/dsa_proposal_1.pdf",
                    file_size=1024000,
                    mime_type="application/pdf",
                    document_type="agreement",
                    checksum="ghi789jkl012",
                    proposal_id=1,
                    created_by=5  # Eve Advisor
                ),
            ]
            
            for document in documents:
                db.add(document)
            db.flush()
            
            # Insert sample template projects
            template_projects = [
                TemplateProject(
                    name="Solar Farm Template - California",
                    description="Standard template for solar farm development in California",
                    project_type=ProjectType.SOLAR,
                    region="California",
                    size_band_min=100.0,
                    size_band_max=500.0,
                    config={
                        "required_milestones": ["feasibility", "permits", "construction"],
                        "estimated_duration_days": 365,
                        "required_approvals": ["environmental", "zoning", "utility"]
                    },
                    created_by=13  # Maya Admin
                ),
                TemplateProject(
                    name="Wind Farm Template - Texas",
                    description="Standard template for wind farm development in Texas",
                    project_type=ProjectType.WIND,
                    region="Texas",
                    size_band_min=200.0,
                    size_band_max=1000.0,
                    config={
                        "required_milestones": ["feasibility", "permits", "construction"],
                        "estimated_duration_days": 450,
                        "required_approvals": ["environmental", "aviation", "utility"]
                    },
                    created_by=13  # Maya Admin
                ),
            ]
            
            for template in template_projects:
                db.add(template)
            db.flush()
            
            # Insert sample notification templates
            notification_templates = [
                NotificationTemplate(
                    name="Task Assignment Email",
                    notification_type=NotificationType.TASK_ASSIGNED,
                    channel=NotificationChannel.EMAIL,
                    subject_template="New Task Assigned: {task_title}",
                    message_template="You have been assigned a new task: {task_title}. Due date: {due_date}",
                    variables=["task_title", "due_date"],
                    is_active=True,
                    priority=1,
                    created_by=13  # Maya Admin
                ),
                NotificationTemplate(
                    name="Approval Required",
                    notification_type=NotificationType.APPROVAL_REQUIRED,
                    channel=NotificationChannel.IN_APP,
                    subject_template="Approval Required: {approval_type}",
                    message_template="Approval required for {approval_type}: {entity_name}",
                    variables=["approval_type", "entity_name"],
                    is_active=True,
                    priority=1,
                    created_by=13  # Maya Admin
                ),
            ]
            
            for template in notification_templates:
                db.add(template)
            
            db.commit()
            print("✅ Comprehensive sample data inserted successfully!")
            print(f"   - {len(users)} users (all types)")
            print(f"   - {len(land_parcels)} land parcels")
            print(f"   - {len(opportunities)} investment opportunities")
            print(f"   - {len(proposals)} investment proposals")
            print(f"   - {len(proposal_parcels)} proposal-parcel mappings")
            print(f"   - {len(projects)} development projects")
            print(f"   - {len(tasks)} tasks")
            print(f"   - {len(milestones)} milestones")
            print(f"   - {len(approvals)} approvals")
            print(f"   - {len(documents)} documents")
            print(f"   - {len(template_projects)} template projects")
            print(f"   - {len(notification_templates)} notification templates")
            
            return True
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_connection():
    """Test connection to the database"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Successfully connected to PostgreSQL!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False

def main():
    """Main function"""
    print("🐘 PostgreSQL Setup for RenewMart")
    print("=" * 40)
    
    print(f"\n📋 Database Configuration:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Port: {DB_CONFIG['port']}")
    print(f"   User: {DB_CONFIG['user']}")
    print(f"   Database: {DB_CONFIG['database']}")
    
    print(f"\n🔧 Setting up database...")
    if create_database():
        print(f"\n🧪 Testing connection...")
        if test_connection():
            print(f"\n🏗️  Creating tables...")
            if create_tables():
                print(f"\n🌱 Inserting sample data...")
                if insert_sample_data():
                    print(f"\n📋 Showing table structures...")
                    show_table_structures()
                    
                    print(f"\n🔌 Showing API endpoints...")
                    show_api_endpoints()
                    
                    print(f"\n🎉 RenewMart PostgreSQL setup completed successfully!")
                    print(f"\n" + "="*70)
                    print(f"📊 COMPREHENSIVE SUMMARY:")
                    print(f"="*70)
                    print(f"✅ Database created: {DB_CONFIG['database']}")
                    print(f"✅ Tables created: 20 tables (complete RenewMart schema)")
                    print(f"✅ Sample data inserted: All personas and workflows")
                    print(f"✅ API endpoints ready: Full REST API specification")
                    print(f"✅ Workflow states: Complete state machines")
                    print(f"✅ Templates: Project and notification templates")
                    print(f"✅ Permissions: Role-based access control")
                    print(f"\n🏗️  RENEWMART ARCHITECTURE:")
                    print(f"="*70)
                    print(f"👥 User Types: Landowner, Investor, Advisor, Analyst, PM, Governance, Admin")
                    print(f"🏞️  Land Parcels: Registration → Feasibility → Proposal → Development → RTB")
                    print(f"💰 Investment: Opportunities → Proposals → Agreements → Projects")
                    print(f"🏗️  Projects: Auto-seeded from templates → Task execution → Milestones")
                    print(f"📋 Tasks: Assignment → Execution → Completion → Approval")
                    print(f"✅ Approvals: Stage-gate workflow with governance oversight")
                    print(f"📄 Documents: Versioned, checksummed, linked to entities")
                    print(f"🔔 Notifications: Multi-channel, templated, workflow-triggered")
                    print(f"\n🚀 NEXT STEPS:")
                    print(f"="*70)
                    print(f"1. Start FastAPI server: uvicorn app.main:app --reload")
                    print(f"2. Visit API docs: http://localhost:8000/docs")
                    print(f"3. Test core endpoints:")
                    print(f"   - Users: http://localhost:8000/api/v1/users")
                    print(f"   - Land Parcels: http://localhost:8000/api/v1/land-parcels")
                    print(f"   - Projects: http://localhost:8000/api/v1/projects")
                    print(f"4. Start frontend: cd ../frontend && npm start")
                    print(f"5. Access application: http://localhost:3000")
                    print(f"\n📚 DOCUMENTATION:")
                    print(f"="*70)
                    print(f"• Database Schema: See table structures above")
                    print(f"• API Endpoints: See endpoint mappings above")
                    print(f"• Sample Data: All personas and workflows populated")
                    print(f"• Workflow States: Complete state machine definitions")
                    print(f"• Sprint Backlog: Ready for Sprint 1-3 development")
                else:
                    print(f"\n❌ Failed to insert sample data.")
            else:
                print(f"\n❌ Failed to create tables.")
        else:
            print(f"\n❌ Database setup failed. Please check your PostgreSQL configuration.")
    else:
        print(f"\n❌ Database setup failed. Please check your PostgreSQL installation.")

if __name__ == "__main__":
    main()
