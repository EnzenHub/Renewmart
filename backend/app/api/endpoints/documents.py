from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import hashlib
import os
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.land_parcel import Document
from app.schemas.land_parcel import Document as DocumentSchema, DocumentCreate
from app.api.endpoints.auth import get_current_user

router = APIRouter()

# File upload settings
UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def calculate_checksum(file_path: str) -> str:
    """Calculate SHA-256 checksum of a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()

@router.get("/", response_model=List[DocumentSchema])
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    document_type: Optional[str] = None,
    land_parcel_id: Optional[int] = None,
    task_id: Optional[int] = None,
    project_id: Optional[int] = None,
    proposal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all documents with optional filtering"""
    query = db.query(Document)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if land_parcel_id:
        query = query.filter(Document.land_parcel_id == land_parcel_id)
    if task_id:
        query = query.filter(Document.task_id == task_id)
    if project_id:
        query = query.filter(Document.project_id == project_id)
    if proposal_id:
        query = query.filter(Document.proposal_id == proposal_id)
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    land_parcel_id: Optional[int] = Form(None),
    task_id: Optional[int] = Form(None),
    project_id: Optional[int] = Form(None),
    proposal_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a new document"""
    
    # Validate file extension
    file_extension = get_file_extension(file.filename)
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File too large")
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Calculate checksum
    checksum = calculate_checksum(file_path)
    
    # Create document record
    document_data = DocumentCreate(
        name=file.filename,
        file_path=file_path,
        file_size=len(content),
        mime_type=file.content_type,
        document_type=document_type,
        checksum=checksum,
        land_parcel_id=land_parcel_id,
        task_id=task_id,
        project_id=project_id,
        proposal_id=proposal_id,
        created_by=current_user.id
    )
    
    db_document = Document(**document_data.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return {
        "message": "Document uploaded successfully",
        "document": DocumentSchema.from_orm(db_document)
    }

@router.get("/{document_id}/download")
async def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")
    
    return {
        "file_path": document.file_path,
        "filename": document.name,
        "mime_type": document.mime_type
    }

@router.put("/{document_id}", response_model=DocumentSchema)
async def update_document(
    document_id: int,
    name: Optional[str] = None,
    document_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update document metadata"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if name:
        document.name = name
    if document_type:
        document.document_type = document_type
    
    db.commit()
    db.refresh(document)
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file from disk
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {document.file_path}: {e}")
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.get("/verify/{document_id}")
async def verify_document_integrity(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify document integrity using checksum"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not os.path.exists(document.file_path):
        return {
            "document_id": document_id,
            "integrity_check": "failed",
            "reason": "File not found on disk"
        }
    
    current_checksum = calculate_checksum(document.file_path)
    is_valid = current_checksum == document.checksum
    
    return {
        "document_id": document_id,
        "integrity_check": "passed" if is_valid else "failed",
        "stored_checksum": document.checksum,
        "current_checksum": current_checksum,
        "is_valid": is_valid
    }
