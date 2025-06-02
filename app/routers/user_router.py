from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services import user_service
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=UserResponse)
def create(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.post("/update/{id}", response_model=UserResponse)
def create(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, id, data)


@router.post("/delete/{id}")
def create(id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, id)


@router.get("/", response_model=list[UserResponse])
def read_posts(db: Session = Depends(get_db)):
    return user_service.get_users(db)
