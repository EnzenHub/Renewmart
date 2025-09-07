#!/usr/bin/env python3
"""
Database Management Script for RenewMart
This script helps you manage the database and view data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.db.database import Base, engine, SessionLocal
from app.models.user import User, Role, Permission, UserRole, RolePermission
from app.models.land_parcel import LandParcel, Document, Task, Approval, Milestone

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def show_tables():
    """Show all tables in the database"""
    print("\n📋 Database Tables:")
    print("-" * 50)
    
    with engine.connect() as conn:
        # For PostgreSQL, query information_schema
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
        """))
        tables = result.fetchall()
        
        for table in tables:
            print(f"• {table[0]}")
    
    print(f"\nTotal tables: {len(tables)}")

def show_data(table_name):
    """Show data from a specific table"""
    print(f"\n📊 Data from {table_name}:")
    print("-" * 50)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name}"))
            rows = result.fetchall()
            
            if not rows:
                print("No data found in this table.")
                return
            
            # Get column names
            columns = result.keys()
            print(f"Columns: {', '.join(columns)}")
            print()
            
            for i, row in enumerate(rows, 1):
                print(f"Row {i}: {dict(row._mapping)}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def insert_sample_data():
    """Insert sample data into the database"""
    print("\n🌱 Inserting sample data...")
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Sample data already exists. Skipping...")
            return
        
        # Insert sample users
        users = [
            User(name="John Doe", email="john@example.com", role="admin"),
            User(name="Jane Smith", email="jane@example.com", role="user"),
            User(name="Bob Johnson", email="bob@example.com", role="manager"),
        ]
        
        for user in users:
            db.add(user)
        
        # Insert sample land parcels
        land_parcels = [
            LandParcel(
                name="Downtown Commercial Lot",
                address="123 Main St, Downtown",
                size="2.5 acres",
                status="active",
                owner="John Doe",
                coordinates={"lat": 40.7128, "lng": -74.0060}
            ),
            LandParcel(
                name="Residential Development",
                address="456 Oak Ave, Suburbs",
                size="5.0 acres",
                status="pending",
                owner="Jane Smith",
                coordinates={"lat": 40.7589, "lng": -73.9851}
            ),
            LandParcel(
                name="Industrial Zone",
                address="789 Industrial Blvd",
                size="10.0 acres",
                status="approved",
                owner="Bob Johnson",
                coordinates={"lat": 40.6892, "lng": -74.0445}
            )
        ]
        
        for parcel in land_parcels:
            db.add(parcel)
        
        db.commit()
        print("✅ Sample data inserted successfully!")
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        db.rollback()
    finally:
        db.close()

def show_all_data():
    """Show data from all tables"""
    print("\n📊 All Database Data:")
    print("=" * 60)
    
    tables = ['users', 'land_parcels', 'roles', 'permissions', 'user_roles', 
              'role_permissions', 'documents', 'tasks', 'approvals', 'milestones']
    
    for table in tables:
        show_data(table)

def main():
    """Main function"""
    print("🗄️  RenewMart Database Manager")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Create tables")
        print("2. Show all tables")
        print("3. Insert sample data")
        print("4. Show all data")
        print("5. Show specific table data")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            create_tables()
        elif choice == '2':
            show_tables()
        elif choice == '3':
            insert_sample_data()
        elif choice == '4':
            show_all_data()
        elif choice == '5':
            table_name = input("Enter table name: ").strip()
            show_data(table_name)
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
