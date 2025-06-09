from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.schemas.post_schema import PostUpdate
from app.utils.error_helper import safe_commit, handle_not_found


def create_post(db: Session, title: str, content: str, user_id: int, image_path: str, heatmap_path: str, count: int):
    query = Post(
        user_id=user_id,
        title=title,
        content=content,
        image=image_path,
        heatmap=heatmap_path,
        count=count
    )
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


def get_posts(db: Session, limit=10, page: int = 0):
    page = page if page > 0 else 1
    page = (page - 1) * limit
    return db.query(Post).order_by(desc(Post.id)).offset(page).limit(limit).all()
