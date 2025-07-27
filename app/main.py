from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import models, schemas, services

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return services.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = services.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = services.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact