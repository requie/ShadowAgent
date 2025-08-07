from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShadowAgent API")

# Enable CORS (adjust origins as needed)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/threats", response_model=List[schemas.Threat])
def read_threats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    threats = crud.get_threats(db, skip=skip, limit=limit)
    return threats

@app.post("/threats", response_model=schemas.Threat)
def create_threat(threat: schemas.ThreatCreate, db: Session = Depends(get_db)):
    return crud.create_threat(db=db, threat=threat)

@app.get("/threats/{threat_id}", response_model=schemas.Threat)
def read_threat(threat_id: int, db: Session = Depends(get_db)):
    db_threat = crud.get_threat(db, threat_id=threat_id)
    if db_threat is None:
        raise HTTPException(status_code=404, detail="Threat not found")
    return db_threat

@app.get("/alerts", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_alerts(db, skip=skip, limit=limit)

@app.post("/threats/{threat_id}/alerts", response_model=schemas.Alert)
def create_alert_for_threat(threat_id: int, alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_threat = crud.get_threat(db, threat_id=threat_id)
    if db_threat is None:
        raise HTTPException(status_code=404, detail="Threat not found")
    return crud.create_alert(db=db, alert=alert, threat_id=threat_id)
