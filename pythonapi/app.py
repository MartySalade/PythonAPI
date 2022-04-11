from email.policy import HTTP
from http.client import HTTPException
from typing import Dict, List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def home() -> Dict:
    return {'hello': 'world'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserCreate:
    db_user = crud.get_user_by_username(db, user_username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.patch("/users/", response_model=schemas.User)
def update_user_username(new_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user_username(db, new_user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)