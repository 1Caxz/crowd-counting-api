from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services import post_service
from app.schemas.post_schema import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=PostResponse)
def create(data: PostCreate, db: Session = Depends(get_db)):
    return post_service.create_post(db, data)


@router.post("/update/{id}", response_model=PostResponse)
def create(id: int, data: PostCreate, db: Session = Depends(get_db)):
    return post_service.update_post(db, id, data)


@router.post("/delete/{id}")
def create(id: int, db: Session = Depends(get_db)):
    return post_service.delete_post(db, id)


@router.get("/list", response_model=list[PostResponse])
def read_posts(db: Session = Depends(get_db)):
    return post_service.get_posts(db)
