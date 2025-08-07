from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


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
