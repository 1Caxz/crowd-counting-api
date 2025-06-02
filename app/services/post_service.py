from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostUpdate
from app.utils.error_helper import safe_commit, handle_not_found

def create_post(db: Session, data: PostCreate):
    query = Post(**data.model_dump())
    db.add(query)
    safe_commit(db, "Post created.")
    db.refresh(query)
    return query

def update_post(db: Session, id: int, data: PostUpdate):
    query = db.query(Post).filter(Post.id == id).first()
    handle_not_found(query, "Post not found.")

    for attr, value in data.model_dump().items():
        setattr(query, attr, value)

    safe_commit(db, "Post updated.")
    db.refresh(query)
    return query

def delete_post(db: Session, id: int):
    query = db.query(Post).filter(Post.id == id).first()
    handle_not_found(query, "Post not found.")
    
    db.delete(query)
    safe_commit(db, "Post deleted.")
    return {"message": "Post deleted."}

def get_posts(db: Session, limit=10):
    return db.query(Post).limit(limit).all()