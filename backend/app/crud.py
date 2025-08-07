from sqlalchemy.orm import Session
from .users import User, WatchedIdentity
from .auth import get_password_hash, verify_password
from typing import Optional

from . import models, schemas


def get_threats(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of threats with pagination."""
    return db.query(models.Threat).offset(skip).limit(limit).all()


def get_threat(db: Session, threat_id: int):
    """Retrieve a single threat by ID."""
    return db.query(models.Threat).filter(models.Threat.id == threat_id).first()


def create_threat(db: Session, threat: schemas.ThreatCreate):
    """Create a new threat and associated alerts."""
    db_threat = models.Threat(
        type=threat.type,
        title=threat.title,
        description=threat.description,
        source=threat.source,
    )
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    # Create alerts if provided
    if threat.alerts:
        for alert in threat.alerts:
            db_alert = models.Alert(
                threat_id=db_threat.id,
                severity=alert.severity,
                message=alert.message,
            )
            db.add(db_alert)
        db.commit()
    db.refresh(db_threat)
    return db_threat


def create_alert(db: Session, threat_id: int, alert: schemas.AlertCreate):
    """Create an alert for a given threat."""
    db_alert = models.Alert(
        threat_id=threat_id,
        severity=alert.severity,
        message=alert.message,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of alerts."""
    return db.query(models.Alert).offset(skip).limit(limit).all()

# User management functions

def get_user(db: Session, user_id: int):
    """Retrieve a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    """Create a new user with hashed password."""
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user and return user if credentials are valid."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_watched_identities(db: Session, user_id: int):
    """Retrieve all watched identities for a user."""
    return db.query(WatchedIdentity).filter(WatchedIdentity.user_id == user_id).all()

def create_watched_identity(db: Session, user_id: int, identifier: str, type: str):
    """Create a new watched identity for a user."""
    db_identity = WatchedIdentity(
        identifier=identifier,
        type=type,
        user_id=user_id,
    )
    db.add(db_identity)
    db.commit()
    db.refresh(db_identity)
    return db_identity
