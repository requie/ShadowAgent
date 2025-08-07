from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from .database import Base


class ThreatType(PyEnum):
    leak = "leak"
    chatter = "chatter"
    breach = "breach"
    other = "other"


class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ThreatType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    source = Column(String, nullable=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)

    alerts = relationship("Alert", back_populates="threat", cascade="all, delete-orphan")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    threat_id = Column(Integer, ForeignKey("threats.id"), nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    threat = relationship("Threat", back_populates="alerts")
