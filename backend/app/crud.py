from sqlalchemy.orm import Session

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
