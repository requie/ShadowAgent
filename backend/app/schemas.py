from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class ThreatType(str, Enum):
    leak = "leak"
    chatter = "chatter"
    breach = "breach"
    other = "other"

class AlertBase(BaseModel):
    severity: str
    message: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    threat_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ThreatBase(BaseModel):
    type: ThreatType
    title: str
    description: Optional[str] = None
    source: Optional[str] = None

class ThreatCreate(ThreatBase):
    alerts: Optional[List[AlertCreate]] = None

class Threat(ThreatBase):
    id: int
    discovered_at: datetime
    alerts: List[Alert] = []

    class Config:
        orm_mode = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Watched identity schemas
class WatchedIdentityBase(BaseModel):
    identifier: str
    type: str

class WatchedIdentityCreate(WatchedIdentityBase):
    pass

class WatchedIdentity(WatchedIdentityBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
