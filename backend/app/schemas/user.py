from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user import UserType

class UserBase(BaseModel):
    name: str
    email: EmailStr
    user_type: UserType
    phone: Optional[str] = None
    company: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[UserType] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_type: UserType

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_type: Optional[UserType] = None

class Role(RoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    resource: str
    action: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None

class Permission(PermissionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserRoleBase(BaseModel):
    user_id: int
    role_id: int

class UserRoleCreate(UserRoleBase):
    pass

class UserRole(UserRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
