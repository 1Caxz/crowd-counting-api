from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.error_handler import safe_commit, handle_not_found

def create_post(db: Session, post: UserCreate):
    db_post = User(**post.model_dump())
    db.add(db_post)
    safe_commit(db, "Membuat post")
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, limit=10):
    return db.query(User).limit(limit).all()