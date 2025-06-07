from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.error_helper import safe_commit, handle_not_found


def create_user(db: Session, data: UserCreate):
    query = User(**data.model_dump())
    db.add(query)
    safe_commit(db, "User created.")
    db.refresh(query)
    return query


def update_user(db: Session, id: int, data: UserUpdate):
    query = db.query(User).filter(User.id == id).first()
    handle_not_found(query, "User not found.")

    for attr, value in data.model_dump().items():
        setattr(query, attr, value)

    safe_commit(db, "User updated.")
    db.refresh(query)
    return query


def delete_user(db: Session, id: int):
    query = db.query(User).filter(User.id == id).first()
    handle_not_found(query, "User not found.")

    db.delete(query)
    safe_commit(db, "User deleted.")
    return {"message": "User deleted."}


def get_users(db: Session, limit=10, page: int = 0):
    page = page if page > 0 else 1
    page = (page - 1) * limit
    return db.query(User).offset(page).limit(limit).all()
