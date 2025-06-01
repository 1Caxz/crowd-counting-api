from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostUpdate
from app.utils.error_handler import safe_commit, handle_not_found

def create_post(db: Session, post: PostCreate):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    safe_commit(db, "Membuat post")
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, new_data: PostUpdate):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    handle_not_found(db_post, "Post tidak ditemukan")

    for attr, value in new_data.model_dump().items():
        setattr(db_post, attr, value)

    safe_commit(db, "Update post")
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    handle_not_found(db_post, "Post tidak ditemukan")
    
    db.delete(db_post)
    safe_commit(db, "Menghapus post")
    return {"message": "Post berhasil dihapus"}