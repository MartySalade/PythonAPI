from typing import Dict, Optional, Sequence

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

description = """
PythonAPI is a small test project to manage FastAPI, SQLAlchemy and Python packages using poetry. 🚀

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
* **Update users usernames** (_not implemented_).
* **Delete users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users using their username, their id or both.",
    },
]

app = FastAPI(
    title="PythonAPI",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)


@app.get("/")
def home() -> Dict:
    return {"Welcome": "Please go to the /docs route to check the API documentation"}


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/users/",
    tags=["users"],
    summary="Get the list of all users.",
    description="The method return the list of all existing users in the database as a Sequence of Users.",
)
def read_users(db: Session = Depends(get_db)) -> Sequence[schemas.User]:
    return crud.get_all_users(db)


@app.get(
    "/users/{id}",
    tags=["users"],
    summary="Get data of a user.",
    description="The method return the user corresponding to the id if it exists, else raise a HTTP Exception",
)
def read_user(id: int, db: Session = Depends(get_db)) -> Sequence[schemas.User]:
    db_user = crud.get_user(db, id)
    if not db_user:
        raise HTTPException(
            status_code=400, detail="User with id: " + str(id) + " doesn't exist"
        )
    return db_user


@app.post(
    "/users/{username}",
    tags=["users"],
    summary="Create a user in the database.",
    description="The method takes a string as a paramater representing the username of the user. It return the created User and raise a HTTP Exception if the username already exists.",
)
def create_user(username: str, db: Session = Depends(get_db)) -> schemas.UserCreate:
    db_user = crud.get_user_by_username(db, user_username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db, username)


@app.patch(
    "/users/{id}&{username}",
    tags=["users"],
    summary="Update the username of an existing user.",
    description="Update the user username by entering as parameters, his id and the new username that will be updated. raise a HTTP Exception if the id doesn't exists in the database.",
)
def update_user_username(
    id: int, username: str, db: Session = Depends(get_db)
) -> Optional[schemas.User]:
    db_user = crud.get_user(db, id)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with id: " + str(id) + " doesn't exists in the database",
        )
    return crud.update_user_username(db, id, username)


@app.delete(
    "/users/{user_id}",
    tags=["users"],
    summary="Delete a user from the database.",
    description="Delete a user from the database using his id. The method raise a HTTP Exception if the id doesn't exists in the database.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> Optional[schemas.User]:
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with id: "
            + str(user_id)
            + " doesn't exists in the database, nothing to delete",
        )
    return crud.delete_user(db, user_id)
