from pyexpat import model
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, user_username: str):
    return db.query(models.User).filter(models.User.username == user_username).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#-------------------------------------------------------------#

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def create_order(db: Session, order: schemas.OrderCreate, _user_id: int):
    db_order = models.Order(**order.dict(), user_id=_user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order