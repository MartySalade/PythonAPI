from typing import List, Optional

from sqlalchemy.orm import Session

from . import models


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, user_username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == user_username).first()


def get_all_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def create_user(db: Session, username: str) -> models.User:
    db_user = models.User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_username(db: Session, id: int, username: str) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == id).one_or_none()
    if db_user is None:
        return None

    db_user.username = username

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).one_or_none()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
