from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    watched_identities = relationship("WatchedIdentity", back_populates="owner", cascade="all, delete-orphan")


class WatchedIdentity(Base):
    __tablename__ = "watched_identities"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, nullable=False)  # e.g., email or domain
    type = Column(String, nullable=False)  # type of identity such as 'email', 'domain', 'ip'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="watched_identities")
