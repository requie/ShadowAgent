from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import status
from datetime import timedelta
from .auth import create_access_token, decode_access_token

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
# Authentication setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, username=user.username, email=user.email, password=user.password)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users/me/identities", response_model=List[schemas.WatchedIdentity])
def read_my_identities(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_watched_identities(db, user_id=current_user.id)

@app.post("/users/me/identities", response_model=schemas.WatchedIdentity)
def create_my_identity(
    identity: schemas.WatchedIdentityCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_watched_identity(
        db, user_id=current_user.id, identifier=identity.identifier, type=identity.type
    )
