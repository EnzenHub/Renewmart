#!/usr/bin/env python3
"""
RenewMart API - Complete Endpoint Testing Script

This script tests all 80+ API endpoints in the RenewMart system.
It demonstrates proper usage, input formats, and expected outputs.

Usage:
    python test_all_endpoints.py

Requirements:
    - Backend server running on http://localhost:8000
    - Database set up with sample data
    - All dependencies installed
"""

import requests
import json
import time
from typing import Dict, Any, Optional
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"
AUTH_BASE = f"{BASE_URL}/api/v1/auth"

# Test data
TEST_USER = {
    "name": "Test User",
    "email": "test@renewmart.com",
    "password": "testpassword123",
    "user_type": "admin",
    "phone": "+1234567890",
    "company": "Test Company"
}

TEST_LAND_PARCEL = {
    "name": "Test Solar Farm",
    "address": "123 Test Street, Test City",
    "size_acres": 10.5,
    "coordinates": {"lat": 40.7128, "lng": -74.0060},
    "description": "Test land parcel for solar development",
    "landowner_id": 1
}

TEST_TASK = {
    "title": "Test Feasibility Study",
    "description": "Conduct feasibility study for test parcel",
    "priority": "high",
    "assigned_to": 1,
    "due_date": "2024-12-31T17:00:00Z",
    "land_parcel_id": 1
}

TEST_OPPORTUNITY = {
    "title": "Test Solar Opportunity",
    "description": "Test solar development opportunity",
    "target_capacity_mw": 50.0,
    "target_region": "Test Region",
    "investment_amount": 25000000.0,
    "expected_roi": 12.0,
    "investor_id": 1
}

TEST_PROPOSAL = {
    "title": "Test Solar Proposal",
    "description": "Test proposal for solar development",
    "total_investment": 25000000.0,
    "expected_roi": 12.0,
    "payback_period_years": 8.0
}

TEST_PROJECT = {
    "name": "Test Solar Project",
    "description": "Test solar development project",
    "project_type": "solar",
    "start_date": "2024-01-01T00:00:00Z",
    "target_completion_date": "2024-12-31T00:00:00Z",
    "budget": 25000000.0,
    "project_manager_id": 1
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_results = []
        
    def log_test(self, endpoint: str, method: str, status_code: int, success: bool, message: str = ""):
        """Log test results"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "success": success,
            "message": message,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {method} {endpoint} - {status_code} - {message}")
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    files: Optional[Dict] = None, params: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{API_BASE}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        if files:
            headers.pop("Content-Type")  # Let requests set multipart boundary
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                if files:
                    response = self.session.post(url, headers=headers, data=data, files=files)
                else:
                    response = self.session.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=headers, json=data)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def test_authentication(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Endpoints")
        print("=" * 50)
        
        # Test login
        login_data = {
            "username": "admin@renewmart.com",
            "password": "admin123"
        }
        
        response = self.session.post(
            f"{AUTH_BASE}/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.log_test("/auth/login", "POST", response.status_code, True, "Login successful")
        else:
            self.log_test("/auth/login", "POST", response.status_code if response else 0, False, "Login failed")
            return False
        
        # Test refresh token
        response = self.make_request("POST", "/auth/refresh")
        self.log_test("/auth/refresh", "POST", response.status_code if response else 0, 
                     response and response.status_code == 200, "Token refresh")
        
        # Test logout
        response = self.make_request("POST", "/auth/logout")
        self.log_test("/auth/logout", "POST", response.status_code if response else 0, 
                     response and response.status_code == 200, "Logout")
        
        return True
    
    def test_user_management(self):
        """Test user management endpoints"""
        print("\n👥 Testing User Management Endpoints")
        print("=" * 50)
        
        # Get all users
        response = self.make_request("GET", "/users/")
        self.log_test("/users/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all users")
        
        # Create user
        response = self.make_request("POST", "/users/", TEST_USER)
        user_id = None
        if response and response.status_code == 201:
            user_id = response.json().get("id")
            self.log_test("/users/", "POST", response.status_code, True, f"User created with ID: {user_id}")
        else:
            self.log_test("/users/", "POST", response.status_code if response else 0, False, "User creation failed")
        
        if user_id:
            # Get specific user
            response = self.make_request("GET", f"/users/{user_id}")
            self.log_test(f"/users/{user_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific user")
            
            # Update user
            update_data = {"name": "Updated Test User"}
            response = self.make_request("PUT", f"/users/{user_id}", update_data)
            self.log_test(f"/users/{user_id}", "PUT", response.status_code if response else 0, 
                         response and response.status_code == 200, "Update user")
            
            # Delete user
            response = self.make_request("DELETE", f"/users/{user_id}")
            self.log_test(f"/users/{user_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete user")
    
    def test_land_parcel_management(self):
        """Test land parcel management endpoints"""
        print("\n🏞️ Testing Land Parcel Management Endpoints")
        print("=" * 50)
        
        # Get all parcels
        response = self.make_request("GET", "/land-parcels/")
        self.log_test("/land-parcels/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all parcels")
        
        # Create parcel
        response = self.make_request("POST", "/land-parcels/", TEST_LAND_PARCEL)
        parcel_id = None
        if response and response.status_code == 201:
            parcel_id = response.json().get("id")
            self.log_test("/land-parcels/", "POST", response.status_code, True, f"Parcel created with ID: {parcel_id}")
        else:
            self.log_test("/land-parcels/", "POST", response.status_code if response else 0, False, "Parcel creation failed")
        
        if parcel_id:
            # Get specific parcel
            response = self.make_request("GET", f"/land-parcels/{parcel_id}")
            self.log_test(f"/land-parcels/{parcel_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific parcel")
            
            # Update parcel
            update_data = {"name": "Updated Test Parcel"}
            response = self.make_request("PUT", f"/land-parcels/{parcel_id}", update_data)
            self.log_test(f"/land-parcels/{parcel_id}", "PUT", response.status_code if response else 0, 
                         response and response.status_code == 200, "Update parcel")
            
            # Assign feasibility study
            feasibility_data = {"analyst_id": 1, "due_date": "2024-12-31T17:00:00Z"}
            response = self.make_request("POST", f"/land-parcels/{parcel_id}/feasibility", feasibility_data)
            self.log_test(f"/land-parcels/{parcel_id}/feasibility", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Assign feasibility study")
            
            # Update parcel status
            status_data = {"new_status": "feasibility_assigned", "comments": "Test status update"}
            response = self.make_request("POST", f"/land-parcels/{parcel_id}/state/transitions", status_data)
            self.log_test(f"/land-parcels/{parcel_id}/state/transitions", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Update parcel status")
            
            # Delete parcel
            response = self.make_request("DELETE", f"/land-parcels/{parcel_id}")
            self.log_test(f"/land-parcels/{parcel_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete parcel")
    
    def test_task_management(self):
        """Test task management endpoints"""
        print("\n📋 Testing Task Management Endpoints")
        print("=" * 50)
        
        # Get all tasks
        response = self.make_request("GET", "/tasks/")
        self.log_test("/tasks/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all tasks")
        
        # Create task
        response = self.make_request("POST", "/tasks/", TEST_TASK)
        task_id = None
        if response and response.status_code == 201:
            task_id = response.json().get("id")
            self.log_test("/tasks/", "POST", response.status_code, True, f"Task created with ID: {task_id}")
        else:
            self.log_test("/tasks/", "POST", response.status_code if response else 0, False, "Task creation failed")
        
        if task_id:
            # Get specific task
            response = self.make_request("GET", f"/tasks/{task_id}")
            self.log_test(f"/tasks/{task_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific task")
            
            # Assign task
            assign_data = {"assignee_id": 1}
            response = self.make_request("PATCH", f"/tasks/{task_id}/assign", assign_data)
            self.log_test(f"/tasks/{task_id}/assign", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Assign task")
            
            # Accept task
            response = self.make_request("PATCH", f"/tasks/{task_id}/accept")
            self.log_test(f"/tasks/{task_id}/accept", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Accept task")
            
            # Complete task
            complete_data = {"completion_notes": "Task completed successfully"}
            response = self.make_request("PATCH", f"/tasks/{task_id}/complete", complete_data)
            self.log_test(f"/tasks/{task_id}/complete", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Complete task")
            
            # Get user tasks
            response = self.make_request("GET", "/tasks/assignee/1")
            self.log_test("/tasks/assignee/1", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get user tasks")
            
            # Delete task
            response = self.make_request("DELETE", f"/tasks/{task_id}")
            self.log_test(f"/tasks/{task_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete task")
    
    def test_document_management(self):
        """Test document management endpoints"""
        print("\n📄 Testing Document Management Endpoints")
        print("=" * 50)
        
        # Get all documents
        response = self.make_request("GET", "/documents/")
        self.log_test("/documents/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all documents")
        
        # Create a test file
        test_file_path = "test_document.txt"
        with open(test_file_path, "w") as f:
            f.write("This is a test document for API testing.")
        
        try:
            # Upload document
            with open(test_file_path, "rb") as f:
                files = {"file": f}
                data = {
                    "document_type": "test_document",
                    "land_parcel_id": "1"
                }
                response = self.make_request("POST", "/documents/upload", data=data, files=files)
            
            document_id = None
            if response and response.status_code == 200:
                document_id = response.json().get("document", {}).get("id")
                self.log_test("/documents/upload", "POST", response.status_code, True, f"Document uploaded with ID: {document_id}")
            else:
                self.log_test("/documents/upload", "POST", response.status_code if response else 0, False, "Document upload failed")
            
            if document_id:
                # Get specific document
                response = self.make_request("GET", f"/documents/{document_id}")
                self.log_test(f"/documents/{document_id}", "GET", response.status_code if response else 0, 
                             response and response.status_code == 200, "Get specific document")
                
                # Download document
                response = self.make_request("GET", f"/documents/{document_id}/download")
                self.log_test(f"/documents/{document_id}/download", "GET", response.status_code if response else 0, 
                             response and response.status_code == 200, "Download document")
                
                # Verify document integrity
                response = self.make_request("GET", f"/documents/verify/{document_id}")
                self.log_test(f"/documents/verify/{document_id}", "GET", response.status_code if response else 0, 
                             response and response.status_code == 200, "Verify document integrity")
                
                # Update document
                update_data = {"name": "Updated Test Document"}
                response = self.make_request("PUT", f"/documents/{document_id}", update_data)
                self.log_test(f"/documents/{document_id}", "PUT", response.status_code if response else 0, 
                             response and response.status_code == 200, "Update document")
                
                # Delete document
                response = self.make_request("DELETE", f"/documents/{document_id}")
                self.log_test(f"/documents/{document_id}", "DELETE", response.status_code if response else 0, 
                             response and response.status_code == 200, "Delete document")
        
        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_approval_workflow(self):
        """Test approval workflow endpoints"""
        print("\n✅ Testing Approval Workflow Endpoints")
        print("=" * 50)
        
        # Get all approvals
        response = self.make_request("GET", "/approvals/")
        self.log_test("/approvals/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all approvals")
        
        # Get pending approvals
        response = self.make_request("GET", "/approvals/pending")
        self.log_test("/approvals/pending", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get pending approvals")
        
        # Create approval
        approval_data = {
            "title": "Test Approval",
            "description": "Test approval request",
            "approval_type": "test",
            "land_parcel_id": 1
        }
        response = self.make_request("POST", "/approvals/", approval_data)
        approval_id = None
        if response and response.status_code == 201:
            approval_id = response.json().get("id")
            self.log_test("/approvals/", "POST", response.status_code, True, f"Approval created with ID: {approval_id}")
        else:
            self.log_test("/approvals/", "POST", response.status_code if response else 0, False, "Approval creation failed")
        
        if approval_id:
            # Get specific approval
            response = self.make_request("GET", f"/approvals/{approval_id}")
            self.log_test(f"/approvals/{approval_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific approval")
            
            # Make approval decision
            decision_data = {"decision": "approve", "comments": "Test approval"}
            response = self.make_request("POST", f"/approvals/{approval_id}/decision", decision_data)
            self.log_test(f"/approvals/{approval_id}/decision", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Make approval decision")
            
            # Cancel approval
            cancel_data = {"reason": "Test cancellation"}
            response = self.make_request("PATCH", f"/approvals/{approval_id}/cancel", cancel_data)
            self.log_test(f"/approvals/{approval_id}/cancel", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Cancel approval")
            
            # Delete approval
            response = self.make_request("DELETE", f"/approvals/{approval_id}")
            self.log_test(f"/approvals/{approval_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete approval")
    
    def test_investment_opportunities(self):
        """Test investment opportunity endpoints"""
        print("\n💰 Testing Investment Opportunity Endpoints")
        print("=" * 50)
        
        # Get all opportunities
        response = self.make_request("GET", "/opportunities/")
        self.log_test("/opportunities/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all opportunities")
        
        # Create opportunity
        response = self.make_request("POST", "/opportunities/", TEST_OPPORTUNITY)
        opportunity_id = None
        if response and response.status_code == 201:
            opportunity_id = response.json().get("id")
            self.log_test("/opportunities/", "POST", response.status_code, True, f"Opportunity created with ID: {opportunity_id}")
        else:
            self.log_test("/opportunities/", "POST", response.status_code if response else 0, False, "Opportunity creation failed")
        
        if opportunity_id:
            # Get specific opportunity
            response = self.make_request("GET", f"/opportunities/{opportunity_id}")
            self.log_test(f"/opportunities/{opportunity_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific opportunity")
            
            # Update opportunity status
            status_data = {"new_status": "under_review", "comments": "Moving to review"}
            response = self.make_request("PATCH", f"/opportunities/{opportunity_id}/state", status_data)
            self.log_test(f"/opportunities/{opportunity_id}/state", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Update opportunity status")
            
            # Get opportunities by investor
            response = self.make_request("GET", "/opportunities/investor/1")
            self.log_test("/opportunities/investor/1", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get opportunities by investor")
            
            # Get opportunities by advisor
            response = self.make_request("GET", "/opportunities/advisor/1")
            self.log_test("/opportunities/advisor/1", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get opportunities by advisor")
            
            # Get opportunities by region
            response = self.make_request("GET", "/opportunities/region/Test%20Region")
            self.log_test("/opportunities/region/Test%20Region", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get opportunities by region")
            
            # Delete opportunity
            response = self.make_request("DELETE", f"/opportunities/{opportunity_id}")
            self.log_test(f"/opportunities/{opportunity_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete opportunity")
    
    def test_investment_proposals(self):
        """Test investment proposal endpoints"""
        print("\n📋 Testing Investment Proposal Endpoints")
        print("=" * 50)
        
        # Get all proposals
        response = self.make_request("GET", "/proposals/")
        self.log_test("/proposals/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all proposals")
        
        # Create proposal for opportunity
        response = self.make_request("POST", "/opportunities/1/proposals", TEST_PROPOSAL)
        proposal_id = None
        if response and response.status_code == 201:
            proposal_id = response.json().get("id")
            self.log_test("/opportunities/1/proposals", "POST", response.status_code, True, f"Proposal created with ID: {proposal_id}")
        else:
            self.log_test("/opportunities/1/proposals", "POST", response.status_code if response else 0, False, "Proposal creation failed")
        
        if proposal_id:
            # Get specific proposal
            response = self.make_request("GET", f"/proposals/{proposal_id}")
            self.log_test(f"/proposals/{proposal_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific proposal")
            
            # Approve proposal
            approve_data = {"comments": "Proposal approved"}
            response = self.make_request("POST", f"/proposals/{proposal_id}/approve", approve_data)
            self.log_test(f"/proposals/{proposal_id}/approve", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Approve proposal")
            
            # Create DSA
            dsa_data = {"agreement_content": "Development Service Agreement terms"}
            response = self.make_request("POST", f"/proposals/{proposal_id}/agreements", dsa_data)
            self.log_test(f"/proposals/{proposal_id}/agreements", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Create DSA")
            
            # Get proposal parcels
            response = self.make_request("GET", f"/proposals/{proposal_id}/parcels")
            self.log_test(f"/proposals/{proposal_id}/parcels", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get proposal parcels")
            
            # Add parcel to proposal
            parcel_data = {"land_parcel_id": 1, "allocation_percentage": 100.0}
            response = self.make_request("POST", f"/proposals/{proposal_id}/parcels", parcel_data)
            self.log_test(f"/proposals/{proposal_id}/parcels", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Add parcel to proposal")
            
            # Delete proposal
            response = self.make_request("DELETE", f"/proposals/{proposal_id}")
            self.log_test(f"/proposals/{proposal_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete proposal")
    
    def test_development_projects(self):
        """Test development project endpoints"""
        print("\n🏗️ Testing Development Project Endpoints")
        print("=" * 50)
        
        # Get all projects
        response = self.make_request("GET", "/projects/")
        self.log_test("/projects/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all projects")
        
        # Create project from proposal
        response = self.make_request("POST", "/proposals/1/projects", TEST_PROJECT)
        project_id = None
        if response and response.status_code == 201:
            project_id = response.json().get("id")
            self.log_test("/proposals/1/projects", "POST", response.status_code, True, f"Project created with ID: {project_id}")
        else:
            self.log_test("/proposals/1/projects", "POST", response.status_code if response else 0, False, "Project creation failed")
        
        if project_id:
            # Get specific project
            response = self.make_request("GET", f"/projects/{project_id}")
            self.log_test(f"/projects/{project_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific project")
            
            # Update project status
            status_data = {"new_status": "in_progress", "comments": "Project started"}
            response = self.make_request("PATCH", f"/projects/{project_id}/status", status_data)
            self.log_test(f"/projects/{project_id}/status", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Update project status")
            
            # Get project milestones
            response = self.make_request("GET", f"/projects/{project_id}/milestones")
            self.log_test(f"/projects/{project_id}/milestones", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get project milestones")
            
            # Create project milestone
            milestone_data = {
                "title": "Test Milestone",
                "description": "Test milestone description",
                "order": 1,
                "target_date": "2024-06-30T00:00:00Z"
            }
            response = self.make_request("POST", f"/projects/{project_id}/milestones", milestone_data)
            milestone_id = None
            if response and response.status_code == 201:
                milestone_id = response.json().get("id")
                self.log_test(f"/projects/{project_id}/milestones", "POST", response.status_code, True, f"Milestone created with ID: {milestone_id}")
            else:
                self.log_test(f"/projects/{project_id}/milestones", "POST", response.status_code if response else 0, False, "Milestone creation failed")
            
            if milestone_id:
                # Submit milestone
                submit_data = {"submission_notes": "Milestone completed"}
                response = self.make_request("POST", f"/projects/{project_id}/milestones/{milestone_id}/submit", submit_data)
                self.log_test(f"/projects/{project_id}/milestones/{milestone_id}/submit", "POST", response.status_code if response else 0, 
                             response and response.status_code == 200, "Submit milestone")
            
            # Get project tasks
            response = self.make_request("GET", f"/projects/{project_id}/tasks")
            self.log_test(f"/projects/{project_id}/tasks", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get project tasks")
            
            # Assign task to project
            task_data = {
                "title": "Test Project Task",
                "description": "Test task for project",
                "priority": "medium",
                "assigned_to": 1,
                "due_date": "2024-12-31T17:00:00Z"
            }
            response = self.make_request("POST", f"/projects/{project_id}/tasks/assign", task_data)
            self.log_test(f"/projects/{project_id}/tasks/assign", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Assign task to project")
            
            # Delete project
            response = self.make_request("DELETE", f"/projects/{project_id}")
            self.log_test(f"/projects/{project_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete project")
    
    def test_configuration_management(self):
        """Test configuration management endpoints"""
        print("\n⚙️ Testing Configuration Management Endpoints")
        print("=" * 50)
        
        # Get project types
        response = self.make_request("GET", "/config/project-types")
        self.log_test("/config/project-types", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get project types")
        
        # Create project type
        project_type_data = {
            "name": "Test Project Type",
            "project_type": "test",
            "region": "Test Region",
            "size_band": "small",
            "description": "Test project type template"
        }
        response = self.make_request("POST", "/config/project-types", project_type_data)
        type_id = None
        if response and response.status_code == 201:
            type_id = response.json().get("id")
            self.log_test("/config/project-types", "POST", response.status_code, True, f"Project type created with ID: {type_id}")
        else:
            self.log_test("/config/project-types", "POST", response.status_code if response else 0, False, "Project type creation failed")
        
        # Get task templates
        response = self.make_request("GET", "/config/templates")
        self.log_test("/config/templates", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get task templates")
        
        # Create task template
        template_data = {
            "name": "Test Task Template",
            "task_type": "test",
            "description": "Test task template",
            "estimated_days": 5,
            "template_project_id": 1
        }
        response = self.make_request("POST", "/config/templates", template_data)
        template_id = None
        if response and response.status_code == 201:
            template_id = response.json().get("id")
            self.log_test("/config/templates", "POST", response.status_code, True, f"Task template created with ID: {template_id}")
        else:
            self.log_test("/config/templates", "POST", response.status_code if response else 0, False, "Task template creation failed")
        
        # Get approval rules
        response = self.make_request("GET", "/config/approval-rules")
        self.log_test("/config/approval-rules", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get approval rules")
        
        # Create approval rule
        rule_data = {
            "name": "Test Approval Rule",
            "project_type": "test",
            "region": "Test Region",
            "size_band": "small",
            "required_approvals": ["governance"],
            "is_active": True
        }
        response = self.make_request("POST", "/config/approval-rules", rule_data)
        rule_id = None
        if response and response.status_code == 201:
            rule_id = response.json().get("id")
            self.log_test("/config/approval-rules", "POST", response.status_code, True, f"Approval rule created with ID: {rule_id}")
        else:
            self.log_test("/config/approval-rules", "POST", response.status_code if response else 0, False, "Approval rule creation failed")
        
        # Get notification templates
        response = self.make_request("GET", "/config/notification-templates")
        self.log_test("/config/notification-templates", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get notification templates")
        
        # Create notification template
        notification_template_data = {
            "name": "Test Notification Template",
            "notification_type": "test",
            "channel": "email",
            "subject": "Test Subject",
            "template": "Test notification template",
            "is_active": True
        }
        response = self.make_request("POST", "/config/notification-templates", notification_template_data)
        notification_template_id = None
        if response and response.status_code == 201:
            notification_template_id = response.json().get("id")
            self.log_test("/config/notification-templates", "POST", response.status_code, True, f"Notification template created with ID: {notification_template_id}")
        else:
            self.log_test("/config/notification-templates", "POST", response.status_code if response else 0, False, "Notification template creation failed")
        
        # Get system health
        response = self.make_request("GET", "/config/system/health")
        self.log_test("/config/system/health", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get system health")
        
        # Clean up created resources
        if rule_id:
            response = self.make_request("DELETE", f"/config/approval-rules/{rule_id}")
            self.log_test(f"/config/approval-rules/{rule_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete approval rule")
    
    def test_notification_system(self):
        """Test notification system endpoints"""
        print("\n🔔 Testing Notification System Endpoints")
        print("=" * 50)
        
        # Get all notifications
        response = self.make_request("GET", "/notifications/")
        self.log_test("/notifications/", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get all notifications")
        
        # Get unread notifications
        response = self.make_request("GET", "/notifications/unread")
        self.log_test("/notifications/unread", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Get unread notifications")
        
        # Create notification
        notification_data = {
            "title": "Test Notification",
            "message": "This is a test notification",
            "notification_type": "test",
            "channel": "email",
            "user_id": 1,
            "data": {"test": "data"}
        }
        response = self.make_request("POST", "/notifications/", notification_data)
        notification_id = None
        if response and response.status_code == 201:
            notification_id = response.json().get("id")
            self.log_test("/notifications/", "POST", response.status_code, True, f"Notification created with ID: {notification_id}")
        else:
            self.log_test("/notifications/", "POST", response.status_code if response else 0, False, "Notification creation failed")
        
        if notification_id:
            # Get specific notification
            response = self.make_request("GET", f"/notifications/{notification_id}")
            self.log_test(f"/notifications/{notification_id}", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get specific notification")
            
            # Mark notification as read
            response = self.make_request("PATCH", f"/notifications/{notification_id}/read")
            self.log_test(f"/notifications/{notification_id}/read", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Mark notification as read")
            
            # Mark notification as unread
            response = self.make_request("PATCH", f"/notifications/{notification_id}/unread")
            self.log_test(f"/notifications/{notification_id}/unread", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Mark notification as unread")
            
            # Mark all notifications as read
            response = self.make_request("PATCH", "/notifications/read-all")
            self.log_test("/notifications/read-all", "PATCH", response.status_code if response else 0, 
                         response and response.status_code == 200, "Mark all notifications as read")
            
            # Get notification statistics
            response = self.make_request("GET", "/notifications/stats/summary")
            self.log_test("/notifications/stats/summary", "GET", response.status_code if response else 0, 
                         response and response.status_code == 200, "Get notification statistics")
            
            # Send notification to user
            send_data = {
                "notification_type": "test",
                "channel": "email",
                "title": "Test Send",
                "message": "Test message",
                "data": {"test": "send"}
            }
            response = self.make_request("POST", "/notifications/send/user/1", send_data)
            self.log_test("/notifications/send/user/1", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Send notification to user")
            
            # Send bulk notifications
            bulk_data = {
                "user_ids": [1, 2],
                "notification_type": "test",
                "channel": "email",
                "title": "Bulk Test",
                "message": "Bulk test message",
                "data": {"test": "bulk"}
            }
            response = self.make_request("POST", "/notifications/send/bulk", bulk_data)
            self.log_test("/notifications/send/bulk", "POST", response.status_code if response else 0, 
                         response and response.status_code == 200, "Send bulk notifications")
            
            # Delete notification
            response = self.make_request("DELETE", f"/notifications/{notification_id}")
            self.log_test(f"/notifications/{notification_id}", "DELETE", response.status_code if response else 0, 
                         response and response.status_code == 200, "Delete notification")
    
    def test_health_endpoints(self):
        """Test health check endpoints"""
        print("\n🏥 Testing Health Check Endpoints")
        print("=" * 50)
        
        # Test basic health check
        response = self.session.get(f"{BASE_URL}/health")
        self.log_test("/health", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "Basic health check")
        
        # Test API health check
        response = self.session.get(f"{API_BASE}/health")
        self.log_test("/api/v1/health", "GET", response.status_code if response else 0, 
                     response and response.status_code == 200, "API health check")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting RenewMart API Comprehensive Testing")
        print("=" * 60)
        
        # Test authentication first
        if not self.test_authentication():
            print("❌ Authentication failed. Cannot proceed with other tests.")
            return
        
        # Run all test suites
        self.test_health_endpoints()
        self.test_user_management()
        self.test_land_parcel_management()
        self.test_task_management()
        self.test_document_management()
        self.test_approval_workflow()
        self.test_investment_opportunities()
        self.test_investment_proposals()
        self.test_development_projects()
        self.test_configuration_management()
        self.test_notification_system()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['method']} {result['endpoint']} - {result['message']}")
        
        print("\n🎉 Testing completed!")

def main():
    """Main function"""
    print("RenewMart API - Complete Endpoint Testing")
    print("=" * 50)
    print("This script will test all 80+ API endpoints")
    print("Make sure the backend server is running on http://localhost:8000")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server is not responding properly")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to backend server. Please start the server first.")
        print("Run: uvicorn app.main:app --reload")
        return
    
    print("✅ Backend server is running")
    
    # Run tests
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
